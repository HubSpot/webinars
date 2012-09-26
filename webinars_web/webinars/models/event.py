from django.db import models as djmodels
from django.db.models import Max,Min
import hapi_plus.leads
#import hapi_plus.contacts
from django.conf import settings
from sanetime.dj import SaneTimeField
from sanetime import time, delta
from segments.models import Criterium, SavedSearch
from webinars_web.webinars.models import mixins
import webex
import gtw
from hapicrank.task_queues import Task
from utils.property import cached_property
import logging

MINUTES_TIL_REGISTRANT_SYNC_STALE = 15
WEBINAR_WINDOW_STOP_PADDING = 2
WEBINAR_WINDOW_START_PADDING = 15


class Event(djmodels.Model, mixins.Event, mixins.Trigger):
    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    account = djmodels.ForeignKey('Account')
    hashcode = djmodels.IntegerField(null=False)
    remote_id = djmodels.CharField(max_length=128, null=True, editable=False)
    alt_remote_id = djmodels.CharField(max_length=128, null=True, editable=False)
    title = djmodels.CharField(max_length=256, null=False)
    description = djmodels.CharField(max_length=2**14-1, null=True)

    _time_starts_at = SaneTimeField(null=True)
    _time_ends_at = SaneTimeField(null=True)
    _time_started_at = SaneTimeField(null=True)
    _time_ended_at = SaneTimeField(null=True)
    _timezone = djmodels.CharField(max_length=64, null=True, editable=False)

    attended_campaign_guid = djmodels.CharField(max_length=36, null=True)
    noshow_campaign_guid = djmodels.CharField(max_length=36, null=True)

    cms_forms = djmodels.ManyToManyField('CmsForm', through='EventForm')
    sync_leads_for_all_time = djmodels.BooleanField(null=False, default=False)
    _update_cms_form = djmodels.ForeignKey('CmsForm', related_name="+", null=True) # no backward relation (would conflict with other one)

    mothballed = djmodels.BooleanField(default=False, null=False)
    unknowable_registrants = djmodels.BooleanField(default=False, null=False)

    _registered_criterium_guid = djmodels.CharField(max_length=36, null=True)
    _attended_criterium_guid = djmodels.CharField(max_length=36, null=True)
    _registered_saved_search_id = djmodels.IntegerField(null=True)
    _attended_saved_search_id = djmodels.IntegerField(null=True)
    _noshow_saved_search_id = djmodels.IntegerField(null=True)

    updated_at = SaneTimeField(auto_now=True)
    created_at = SaneTimeField(auto_now_add=True)
    deleted_at = SaneTimeField(null=True, editable=False)

    last_sync = djmodels.ForeignKey('EventSync', null=True, related_name='+')
    current_sync = djmodels.ForeignKey('EventSync', null=True, related_name='+')
    sync_lock = djmodels.CharField(max_length=36, null=True)


    def sync(self, force=False, visible=False, debug=False, parent_sync=None):
        if force: self.shutdown_all_syncs()
        from webinars_web.webinars import models as wm
        event_sync = wm.EventSync.objects.create(event=self, visible=visible, debug=debug, parent=parent_sync)
        if not debug:
            path = '%s%s' % (settings.APP_URL,event_sync.kickoff_path)
            real_id = 'event_sync|kickoff|%s'%event_sync.id
            logging.debug('TQDEBUG: path is %s' % path)
            logging.debug('TQDEBUG: event_sync id is %s' % real_id)
            qid = self.account_id % settings.NUM_QUEUES
            logging.debug('TQDEBUG: qid is %s' % qid)
            Task(queue=settings.TASK_QUEUES[qid], url=path, method='POST', uid=real_id).enqueue(max_retries=5)
        return event_sync


    def pre_sync_hook(self, sync):
        from webinars_web.webinars import models as wm
        if self.mothballed: return False
        if self.account.is_webex:
            if self.starts_at < time()-delta(md=89): # past webex registrant/attendee reporting limit (90 days)
                self.unknowable_registrants = True
                self.mothballed = True
                self.save()
                return False
        if not self._lock_for_sync():
            if sync.visible and self.current_sync and not self.current_sync.visible:
                wm.EventSync.objects.filter(id=self.current_sync.id).update(visible=True)
            return False
        self.__class__.objects.filter(id=self.id).update(current_sync=sync)
        self.current_sync = sync # faster than changing attr and save()-ing
        return True


    def shutdown_all_syncs(self):
        from webinars_web.webinars import models as wm
        now = time()
        wm.EventSync.objects.filter(completed_at__isnull=True, event=self).update(completed_at=now, forced_stop=True)
        wm.GTWEventSyncStage.objects.filter(completed_at__isnull=True, parent_sync__event=self).update(completed_at=now)
        wm.WebexEventSyncStage.objects.filter(completed_at__isnull=True, parent_sync__event=self).update(completed_at=now)
        wm.HubSpotEventSyncStage.objects.filter(completed_at__isnull=True, parent_sync__event=self).update(completed_at=now)
        wm.EventSyncShard.objects.filter(completed_at__isnull=True, parent_sync__event=self).update(completed_at=now)
        if self.current_sync or self.sync_lock:
            self.__class__.objects.filter(pk=self.id).update(current_sync=None, sync_lock=None)
            self.current_sync = self.sync_lock = None


    def post_sync_hook(self, started_at, completed_at):
        if started_at > self.ended_at:
            if not self.registrant_set.filter(lead_guid__isnull=True, deleted_at__isnull=True).count():
                if self._ended_at or self.ends_at and self.ends_at < time()-delta(md=2):
                    self.mothballed = True
                    self.save()


    @property
    def visible_cms_forms(self):
        return [cf for cf in self.cms_forms.all() if not cf.is_sync_target]

    def __unicode__(self):
        return self.title

    @property
    def update_cms_form(self):
        from webinars_web.webinars.models import EventForm, CmsForm
        if not self._update_cms_form:
            possibles = self.cms_forms.filter(is_sync_target=True)
            if possibles:
                self._update_cms_form = possibles[0]
            else:
                title = "%s [Webinars Sync]" % self.title
                
                #reg_prop_title = "%s [registered]" % self.id
                #att_prop_title = "%s [attended]" % self.id
                #nos_prop_title = "%s [noshow]" % self.id

                leads_client = hapi_plus.leads.LeadsClient(settings.HUBSPOT_API_KEY, hub_id=self.account.hub.id, env=settings.API_ENV, timeout=30)
                
                #contacts_client = hapi_plus.contacts.ContactsClient(settings.HUBSPOT_API_KEY, hub_id=self.account.hub.id, env=settings.API_ENV, timeout=30)
                
                form_guid = leads_client.create_form(title)['guid']
                cms_form = CmsForm(hub=self.account.hub, guid=form_guid, name=title, is_sync_target=True)
                cms_form.save()
                event_form = EventForm(event=self, cms_form=cms_form)
                event_form.save()
                self._update_cms_form = cms_form
            self.save()
        return self._update_cms_form

    def sync_shard(self, depth, section):
        from cynq import Controller, Arm, FacetStore
        skip_hubspot = self.account.exclude_old_events_from_hubspot and self.account.exclusion_date and self.starts_at.us < self.account.exclusion_date.us
        if self.account.is_webex:
            from webinars_web.webinars.cynq.registrant import RegistrantLocalStore, WebexRegistrantSnapshotStore, HubSpotRegistrantSnapshotStore
            from webinars_web.webinars.cynq.registrant import WebexRegistrantSpec, HubSpotRegistrantSpec, WebexRegistrantRemoteStore, HubSpotRegistrantRemoteStore

            local = RegistrantLocalStore(self, depth, section)
            arms = []
            webex_spec = WebexRegistrantSpec()
            webex_snapshot = WebexRegistrantSnapshotStore(self, depth, section)
            webex_remote = WebexRegistrantRemoteStore(self, depth, section)
            webex_local = FacetStore(local)
            arms.append(Arm(webex_spec, webex_remote, webex_local, webex_snapshot))
            
            if not skip_hubspot:
                hubspot_spec = HubSpotRegistrantSpec()
                hubspot_snapshot = HubSpotRegistrantSnapshotStore(self, depth, section)
                hubspot_remote = HubSpotRegistrantRemoteStore(self, depth, section)
                hubspot_local = FacetStore(local)
                arms.append(Arm(hubspot_spec, hubspot_remote, hubspot_local, hubspot_snapshot))
            else:
                logging.debug('SYNCDEBUG: skipping hubspot arm for event with id=%s' % self.id)
        elif self.account.is_gtw:
            from webinars_web.webinars.cynq.registrant import RegistrantLocalStore, GTWRegistrantSnapshotStore, HubSpotRegistrantSnapshotStore
            from webinars_web.webinars.cynq.registrant import GTWRegistrantSpec, HubSpotRegistrantSpec, GTWRegistrantRemoteStore, HubSpotRegistrantRemoteStore

            local = RegistrantLocalStore(self, depth, section)
            arms = []
            gtw_spec = GTWRegistrantSpec()
            gtw_snapshot = GTWRegistrantSnapshotStore(self, depth, section)
            gtw_remote = GTWRegistrantRemoteStore(self, depth, section)
            gtw_local = FacetStore(local)
            arms.append(Arm(gtw_spec, gtw_remote, gtw_local, gtw_snapshot))

            if not skip_hubspot:
                hubspot_spec = HubSpotRegistrantSpec()
                hubspot_snapshot = HubSpotRegistrantSnapshotStore(self, depth, section)
                hubspot_remote = HubSpotRegistrantRemoteStore(self, depth, section)
                hubspot_local = FacetStore(local)
                arms.append(Arm(hubspot_spec, hubspot_remote, hubspot_local, hubspot_snapshot))
            else:
                logging.debug('SYNCDEBUG: skipping hubspot arm for event with id=%s' % self.id)
        return Controller(*arms).cynq()


    @property
    def settings(self): return settings

    @property
    def event_forms(self):
        return self.eventform_set.all()

    @property
    def prevent_unformed_lead_import(self):
        return self.account.prevent_unformed_lead_import
        
    @classmethod
    def cleanup_stuck_syncs(kls):
        pass # TODO: implement
        #recency_limit = (sanetime()-1000**2*60*MINUTES_TIL_EVENT_SYNC_STALE)
        #for hub in Hub.objects.filter(Q(events_synced_at__lt = recency_limit) | Q(events_synced_at__isnull=True)):
            #hub.queue_cascading_events_sync(priority)

    @property
    def registered_this_form_key(self):
        return 'XAPP_Webinars_RT_%s_%s' % (self.account.account_type_id, self.remote_id)

    @property
    def registered_this_form_label(self):
        return 'Registered For "%s"(%s) Webinar?' % (self.title, self.starts_at.strftime("%m/%d/%y"))

    @property
    def attended_this_form_key(self):
        return 'XAPP_Webinars_AT_%s_%s' % (self.account.account_type_id, self.remote_id)

    @property
    def attended_this_form_label(self):
        return 'Attended "%s"(%s) Webinar?' % (self.title, self.starts_at.strftime("%m/%d/%y"))

    @property
    def registered_criterium_guid(self):
        if not self._registered_criterium_guid:
            self._ensure_segment_info()
        return self._registered_criterium_guid

    @property
    def attended_criterium_guid(self):
        if not self._attended_criterium_guid:
            self._ensure_segment_info()
        return self._attended_criterium_guid

    @property
    def registered_saved_search_id(self):
        if not self._registered_saved_search_id:
            self._ensure_segment_info()
        return self._registered_saved_search_id

    @property
    def attended_saved_search_id(self):
        if not self._attended_saved_search_id:
            self._ensure_segment_info()
        return self._attended_saved_search_id

    @property
    def noshow_saved_search_id(self):
        if not self._noshow_saved_search_id:
            self._ensure_segment_info()
        return self._noshow_saved_search_id

    @property
    def registered_segment_url(self):
        return "https://app.hubspot%s.com/*/create?portalId=%s&savedListId=%s" % (
                settings.ENV != 'prod' and 'qa' or '',
                self.account.hub_id, 
                self.registered_saved_search_id )

    @property
    def attended_segment_url(self):
        return "https://app.hubspot%s.com/*/create?portalId=%s&savedListId=%s" % (
                settings.ENV != 'prod' and 'qa' or '',
                self.account.hub_id, 
                self.attended_saved_search_id )

    @property
    def noshow_segment_url(self):
        return "https://app.hubspot%s.com/*/create?portalId=%s&savedListId=%s" % (
                settings.ENV != 'prod' and 'qa' or '',
                self.account.hub_id, 
                self.noshow_saved_search_id )


    def _ensure_segment_info(self):
        self._registered_criterium_guid = Criterium.ensure_existence (
            guid = self._registered_criterium_guid,
            hub_id = self.account.hub_id,
            field_id = 1,
            label = self.registered_this_form_label,
            field_keys_json = '["%s"]' % self.registered_this_form_key,
            field_values_json = '["Yes"]' )
        self._registered_saved_search_id = SavedSearch.ensure_existence(
            hub_id = self.account.hub_id,
            saved_search_id = self._registered_saved_search_id,
            name = 'Webinar Registrants For (%s) "%s"' % (self.starts_at.strftime("%m/%d/%y"), self.title),
            criterium_guid = self.registered_criterium_guid,
            value = 'Yes' )
        self._attended_criterium_guid = Criterium.ensure_existence (
            guid = self._attended_criterium_guid,
            hub_id = self.account.hub_id,
            field_id = 1,
            label = self.attended_this_form_label,
            field_keys_json = '["%s"]' % self.attended_this_form_key,
            field_values_json = '["Yes","No"]' )
        self._attended_saved_search_id = SavedSearch.ensure_existence(
            hub_id = self.account.hub_id,
            saved_search_id = self._attended_saved_search_id,
            name = 'Webinar Attendees For (%s) "%s"' % (self.starts_at.strftime("%m/%d/%y"), self.title),
            criterium_guid = self.attended_criterium_guid,
            value = 'Yes' )
        self._noshow_saved_search_id = SavedSearch.ensure_existence(
            hub_id = self.account.hub_id,
            saved_search_id = self._noshow_saved_search_id,
            name = 'Webinar Noshows For (%s) "%s"' % (self.starts_at.strftime("%m/%d/%y"), self.title),
            criterium_guid = self.attended_criterium_guid,
            value = 'No' )
        self.save()

    @property
    def webex_event(self):
        return webex.event.Event(self.account.webex_account, title=self.title, starts_at=self.starts_at, duration=self.duration.m, description=self.description, session_key=self.remote_id)

    @property
    def gtw_session(self):
        webinar = gtw.Webinar(self.account.gtw_organizer, key=self.remote_id.split('-')[0], subject=self.title, description=self.description, timezone=self._timezone)
        session = gtw.Session(webinar, key=self.alt_remote_id, starts_at=self._time_starts_at, ends_at=self._time_ends_at, started_at=self._time_started_at, ended_at=self._time_ended_at) 
        return session


    @property
    def start_caring_at(self):
        if not self._time_started_at: return None
        return min(self._time_starts_at, self.registrants_min_max_start_stop[0])

    @property
    def stop_caring_at(self):
        if not self._time_ended_at: return None
        return max(self._time_ends_at, self.registrants_min_max_start_stop[1])

    @cached_property
    def registrants_min_max_start_stop(self):
        min_max = self.registrant_set.filter(deleted_at__isnull=True, started_at__isnull=False).aggregate(Min('started_at'),Max('stopped_at'))
        return (time(us=(min_max['started_at__min'] or self._time_starts_at.us)), time(us=(min_max['stopped_at__max'] or self._time_ends_at.us)))
        
    @property
    def caring_duration(self): return self.start_caring_at and self.stop_caring_at and self.stop_caring_at-self.start_caring_at

    @property
    def starts_at_care_percentage(self): return self.starts_at and self.caring_duration and int(self.starts_at-self.start_caring_at)*100.0/int(self.caring_duration)

    @property
    def ends_at_care_percentage(self): return self.ends_at and self.caring_duration and int(self.ends_at-self.start_caring_at)*100.0/int(self.caring_duration)

    @property
    def deletable(self): return self.account.is_webex

    @property
    def editable_details(self): return self.account.is_webex

    @property
    def title_truncated(self): return '%s...'%self.title[0:60] if self.title and len(self.title)>60 else self.title



    def expunge(self):
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute('UPDATE webinars_event SET last_sync_id=NULL, current_sync_id=NULL, sync_lock=NULL WHERE id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_gtweventsyncstage WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_webexeventsyncstage WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_hubspoteventsyncstage WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_eventsyncshard WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_eventsync WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_registrant WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_gtwregistrantsnapshot WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_webexregistrantsnapshot WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_hubspotregistrantsnapshot WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_stagedgtwregistrant WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_stagedwebexregistrant WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_stagedhubspotregistrant WHERE event_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_event WHERE id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_webexeventsnapshot WHERE remote_id in (SELECT DISTINCT remote_id FROM webinars_event WHERE id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_stagedwebexevent WHERE session_key in (SELECT DISTINCT remote_id FROM webinars_event WHERE id=%s)', [self.id])
        
        transaction.commit_unless_managed()
    
