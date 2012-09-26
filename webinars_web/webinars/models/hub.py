from operator import attrgetter
from django.db import models
from django.conf import settings
from sanetime import delta,time
from sanetime.dj import SaneTimeField
from segments.models import Criterium, SavedSearch
from webinars_web.webinars.models import mixins
#import logging
from cake import Hub as SettingsHub,env  #must keep env here for now
from giftwrap import Exchange
from sfdc_info.models import Trial,Subscription
import logging

MINUTES_TIL_STALE_SYNC = 15


class Hub(models.Model, mixins.Trigger):
    class Meta:
        app_label = 'webinars'

    id = models.BigIntegerField(primary_key=True, unique=True)

    _timezone = models.CharField(max_length=64, null=True)
    _cms_domain = models.CharField(max_length=256, null=True)
    uninstalled_at = SaneTimeField(null=True)

    _registered_any_criterium_guid = models.CharField(max_length=36, null=True)
    _attended_any_criterium_guid = models.CharField(max_length=36, null=True)
    _registered_any_saved_search_id = models.IntegerField(null=True)
    _attended_any_saved_search_id = models.IntegerField(null=True)

    updated_at = SaneTimeField(auto_now=True)
    created_at = SaneTimeField(auto_now_add=True)

    last_sync = models.ForeignKey('HubSync', null=True, related_name='+')
    current_sync = models.ForeignKey('HubSync', null=True, related_name='+')
    sync_lock = models.CharField(max_length=36, null=True)

    internal = models.BooleanField(null=False)
    beta = models.BooleanField(null=False)
    paused = models.BooleanField(null=False, default=False)

    _friends_and_family = models.BooleanField(null=False, default=False)
    _churned_at = SaneTimeField(null=True)
    _product_type = models.CharField(null=True, max_length=255)
    _sfdc_info_at = SaneTimeField(null=True)

    @property
    def has_webex_account(self): return self.account_set.filter(deleted_at__isnull=True, account_type=1)

    @property
    def has_gtw_account(self): return self.account_set.filter(deleted_at__isnull=True, account_type=2)

    @classmethod
    def sync_all(kls):
        candidates = kls.objects.filter(uninstalled_at__isnull=True, paused=False).select_related('last_sync')
        logging.debug("SYNCALL: %s candidates found at %s" % (len(candidates), time()))
        qualified = []
        for c in candidates:
            if c.current_sync and c.current_sync.is_bad:
                s = c.sync(force=True)
                if s: qualified.append(s)
            elif not c.current_sync:
                s = c.sync()
                if s: qualified.append(s)
        # we also want to sync stuff that is hung for more than an hour
        logging.debug("SYNCALL: %s qualified candidated found at %s" % (len(qualified), time()))
        return qualified

    # This property doesn't seem to get used anywhere...
    @property
    def sync_overdue(self):
        if self.uninstalled_at or self.current_sync: return False
        if not self.last_sync: return True
        return not self.last_sync or (time() - self.last_sync.completed_at) > delta(m=MINUTES_TIL_STALE_SYNC)  # greater than 15 minutes

    def sync(self, force=False, visible=False, debug=False):
        from webinars_web.webinars import models as wm
        if self.uninstalled_at: return None
        if self.account_set.filter(deleted_at__isnull=True).count() == 0: return None
        if force: self.shutdown_all_syncs()
        if not self._lock_for_sync(): 
            if visible and self.current_sync and not self.current_sync.visible:
                wm.HubSync.objects.filter(id=self.current_sync.id).update(visible=visible)
            return None
        hub_sync = wm.HubSync.objects.create(hub=self, visible=visible, debug=debug)
        self.__class__.objects.filter(pk=self.id).update(current_sync=hub_sync)
        self.current_sync = hub_sync
        return hub_sync.start()

    def shutdown_all_syncs(self):
        from webinars_web.webinars import models as wm
        now = time()
        wm.HubSync.objects.filter(completed_at__isnull=True, hub=self).update(completed_at=now, forced_stop=True)
        for account in self.account_set.filter(deleted_at__isnull=True):
            account.shutdown_all_syncs()
        if self.current_sync or self.sync_lock:
            self.__class__.objects.filter(pk=self.id).update(current_sync=None, sync_lock=None)
            self.current_sync = self.sync_lock = None


    def __unicode__(self):
        return "Hub ID: %s" % self.id


    @property
    def timezone(self): return self._ensure_settings_info() and self._timezone
    @property
    def cms_domain(self): return self._ensure_settings_info() and self._cms_domain

    def _ensure_settings_info(self, settingshub=None):
        if settingshub or self._timezone is None:
            settingshub = settingshub or SettingsHub(id=self.id, api_key=settings.HUBSPOT_API_KEY, env=settings.API_ENV)
            self._cms_domain = settingshub.cms_domain
            self._timezone = settingshub.timezone or 'America/New_York'
            self.save()
        return self._timezone

    @classmethod
    def _bulk_settings_fill(self):
        from webinars_web.webinars import models as wm
        hubs_settingshubs = [(h, SettingsHub(id=h.id, api_key=settings.HUBSPOT_API_KEY, env=settings.API_ENV)) for h in wm.Hub.objects.all()]
        Exchange.async_exchange([hs[1].settings.scope(domains=True)._settings_ex for hs in hubs_settingshubs])
        for h,s in hubs_settingshubs:
            h._ensure_settings_info(s)



    @property
    def friends_and_family(self): return self._ensure_sfdc_info() and self._friends_and_family
    @property
    def churned_at(self): return self._ensure_sfdc_info() and self._churned_at
    @property
    def product_type(self): return self._ensure_sfdc_info() and self._product_type

    def _ensure_sfdc_info(self, trial=None,subscription=None):
        if (trial and subscription) or self._sfdc_info_at is None:
            if not trial:
                possibles = Trial.objects.filter(_hub_id=str(self.id))
                trial = possibles and possibles[0]
            if not subscription:
                possibles = Subscription.objects.filter(_hub_id=str(self.id))
                subscription = possibles and possibles[0]
            if trial:
                self._friends_and_family = trial.friends_and_family
                self._churned_at = trial.churned_at
                self._product_type = trial.product_type
            if subscription:
                self._churned_at = subscription.churned_at or self._churned_at
                self._product_type = subscription.product or self._product_type
            self._sfdc_info_at = time()
            self.save()
        return self._sfdc_info_at

    @classmethod
    def _bulk_sfdc_info_fill(self):
        from webinars_web.webinars import models as wm
        hub_map = dict((h.id,h) for h in wm.Hub.objects.all())
        trials = dict((t.hub_id,t) for t in Trial.objects.filter(_hub_id__in=hub_map.keys()))
        subscriptions = dict((s.hub_id,s) for s in Subscription.objects.filter(_hub_id__in=hub_map.keys()))
        for h in hub_map.values():
            h._ensure_sfdc_info(trial=trials.get(h.id),subscription=subscriptions.get(h.id))


    @property
    def install_delta(self): return (self.uninstalled_at or time()) - self.created_at


    @property
    def events(self):
        from webinars_web.webinars.models import Event
        return sorted(Event.objects.filter(account__hub=self, deleted_at__isnull=True), key=attrgetter('starts_at'), reverse=True)

    @property
    def accounts(self):
        return self.account_set.filter(deleted_at__isnull=True)

    def sync_forms(self):
        from webinars_web.webinars.models import CmsForm
        CmsForm.sync(self)

    def uninstall(self):
        self.uninstalled_at = time()
        self.save()
        logging.debug("uninstalled app for hub %s at %s" % (self.id, self.uninstalled_at))

    def _get_last_synced_at(self):
        return self.last_sync and self.last_sync.completed_at
    last_synced_at = property(_get_last_synced_at)


    #TODO: need to set up timezone from settings API on initialization
    #TODO: need to make sure all Hub initialization happens in that spot

    @classmethod
    def cleanup_stuck_syncs(kls):
        pass # TODO: implement
        #recency_limit = (sanetime()-1000**2*60*MINUTES_TIL_EVENT_SYNC_STALE)
        #for hub in Hub.objects.filter(Q(events_synced_at__lt = recency_limit) | Q(events_synced_at__isnull=True)):
            #hub.queue_cascading_events_sync(priority)

    @classmethod
    def ensure(kls, hub_id, installed=True, select_related=None):
        query = kls.objects
        if select_related: query = query.select_related(*select_related)
        hub = query.get_or_create(id=hub_id)[0]
        if installed and hub.uninstalled_at:
            hub.uninstalled_at = None
            hub.save()
        return hub

    def _get_registered_any_form_key(self):
        return 'XAPP_Webinars_RA'
    registered_any_form_key = property(_get_registered_any_form_key)

    def _get_registered_any_form_label(self):
        return 'Registered For Any Webinar?'
    registered_any_form_label = property(_get_registered_any_form_label)

    def _get_attended_any_form_key(self):
        return 'XAPP_Webinars_AA'
    attended_any_form_key = property(_get_attended_any_form_key)

    def _get_attended_any_form_label(self):
        return 'Attended Any Webinar?'
    attended_any_form_label = property(_get_attended_any_form_label)

    def _get_registered_any_criterium_guid(self):
        if not self._registered_any_criterium_guid:
            self._ensure_segment_info()
        return self._registered_any_criterium_guid
    registered_any_criterium_guid = property(_get_registered_any_criterium_guid)

    def _get_attended_any_criterium_guid(self):
        if not self._attended_any_criterium_guid:
            self._ensure_segment_info()
        return self._attended_any_criterium_guid
    attended_any_criterium_guid = property(_get_attended_any_criterium_guid)

    def _get_registered_any_saved_search_id(self):
        if not self._registered_any_saved_search_id:
            self._ensure_segment_info()
        return self._registered_any_saved_search_id
    registered_any_saved_search_id = property(_get_registered_any_saved_search_id)

    def _get_attended_any_saved_search_id(self):
        if not self._attended_any_saved_search_id:
            self._ensure_segment_info()
        return self._attended_any_saved_search_id
    attended_any_saved_search_id = property(_get_attended_any_saved_search_id)

    def _get_registered_any_segment_url(self):
        return "https://app.hubspot%s.com/*/create?portalId=%s&savedListId=%s" % (
                settings.ENV != 'prod' and 'qa' or '',
                self.id, 
                self.registered_any_saved_search_id )
    registered_any_segment_url = property(_get_registered_any_segment_url)

    def _get_attended_any_segment_url(self):
        return "https://app.hubspot%s.com/*/create?portalId=%s&savedListId=%s" % (
                settings.ENV != 'prod' and 'qa' or '',
                self.id, 
                self.attended_any_saved_search_id )
    attended_any_segment_url = property(_get_attended_any_segment_url)

    def _ensure_segment_info(self):
        self._registered_any_criterium_guid = Criterium.ensure_existence(
            guid = self._registered_any_criterium_guid,
            hub_id = self.id,
            field_id = 1,
            label = self.registered_any_form_label,
            field_keys_json = '["%s"]' % self.registered_any_form_key,
            field_values_json = '["Yes"]' )

        self._attended_any_criterium_guid = Criterium.ensure_existence(
            guid = self._attended_any_criterium_guid,
            hub_id = self.id,
            field_id = 1,
            label = self.attended_any_form_label,
            field_keys_json = '["%s"]' % self.attended_any_form_key,
            field_values_json = '["Yes"]' )

        self._registered_any_saved_search_id = SavedSearch.ensure_existence(
            hub_id = self.id,
            saved_search_id = self._registered_any_saved_search_id,
            name = 'Webinar Registrants For All Time',
            criterium_guid = self.registered_any_criterium_guid,
            value = 'Yes' )

        self._attended_any_saved_search_id = SavedSearch.ensure_existence(
            hub_id = self.id,
            saved_search_id = self._attended_any_saved_search_id,
            name = 'Webinar Attendees For All Time',
            criterium_guid = self.attended_any_criterium_guid,
            value = 'Yes' )
        self.save()
        

    #def sync(self, force=True, extreme_force=False):
        #if not self.uninstalled_at:
            #for account in self.account_set.all():
                #if extreme_force or (force or account.is_sync_due) and not account.is_sync_ongoing:
                    #account.trigger_sync(force=account.is_sync_ongoing)

    #@classmethod
    #def sync_all(kls, force=False, extreme_force=False):
        #from webinars_web.webinars import models as wm
        #for account in wm.Account.objects.filter(hub__uninstalled_at__isnull=True):
            #if extreme_force or (force or account.is_sync_due) and not account.is_sync_ongoing:
                #account.trigger_sync(force=account.is_sync_ongoing)

    #def _get_has_recent_account_addition(self):
        #last_account_created_at = self.account_set.values_list('created_at', flat=True).order_by('-created_at')[0]
        #return sanetime() - last_account_created_at < 30*10**6  # within 30 seconds
    #has_recent_account_addition = property(_get_has_recent_account_addition)

