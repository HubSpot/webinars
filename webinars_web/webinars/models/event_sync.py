from django.db import models
from django.conf import settings
from sanetime import time,delta
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import BaseSync
from utils.property import cached_property

class EventSync(BaseSync):
    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    created_at = SaneTimeField(auto_now_add=True)
    started_at = SaneTimeField(null=True)
    event = models.ForeignKey('Event', null=False)
    parent = models.ForeignKey('AccountSync', null=True)

    @cached_property
    def webex_stages(self): 
        return self.webexeventsyncstage_set.select_related('parent_sync').all()

    @cached_property
    def gtw_stages(self): 
        return self.gtweventsyncstage_set.select_related('parent_sync').all()

    @cached_property
    def hubspot_stages_cmsforms(self):
        d = {}
        for stage in self.hubspoteventsyncstage_set.select_related('parent_sync','event_form','event_form__cms_form').order_by('start_last_modified_at','offset'):
            d.setdefault(stage.event_form.cms_form,[]).append(stage)
        return [(v,k) for k,v in d.iteritems()]

    @cached_property
    def shards(self): 
        return self.eventsyncshard_set.all()
    #extra(select={'position': 'section/depth'}).order_by('position')

    def start(self):
        from webinars_web.webinars import models as wm
        now = time()
        self.__class__.objects.filter(id=self.id).update(started_at=now)
        self.started_at = now
        if not self.event.pre_sync_hook(self):
            self.completed_at = time()
            self.save()
            return self
        if self.event.account.is_webex:
            wm.StagedWebexRegistrant.pre_stage(self.event)
            wm.WebexEventSyncStage.trigger_initial_stages(self)
        elif self.event.account.is_gtw:
            wm.StagedGTWRegistrant.pre_stage(self.event)
            wm.GTWEventSyncStage.trigger_initial_stages(self)

        wm.StagedHubSpotRegistrant.pre_stage(self.event)
        for event_form in self.event.event_forms.all():
            if time() > max(self.event.ended_at,self.event.ends_at)+delta(m=30) and not event_form.cms_form.is_sync_target: continue # avoid pulling any more leads after event is over
            wm.HubSpotEventSyncStage.objects.create(parent_sync=self, max_size=settings.HUBSPOT_EVENT_SYNC_STAGE_SIZE, event_form=event_form, start_last_modified_at=event_form.last_last_modified_at).trigger()
        #TODO: figure out what to do when cms form goes away-- maybe need to soft delete forms to keep them from violating foreign key constraints on old syncs?
        self.event.update_cms_form  # establishes its existence-- this is a good place to do it-- don't let the individual shards do it cuz then there are async issues to contend with 

        return self


    def possibly_staged(self):
        if self.completed_at: return None
        if self.event.account.is_webex:
            if self.webexeventsyncstage_set.filter(completed_at__isnull=True).count(): return None
        elif self.event.account.is_gtw:
            if self.gtweventsyncstage_set.filter(completed_at__isnull=True).count(): return None
        if self.hubspoteventsyncstage_set.filter(completed_at__isnull=True).count(): return None

        now = time()
        locked = (self.__class__.objects.filter(id=self.id, staged_at__isnull=True).update(staged_at=now) == 1)
        if not locked: return None
        self.staged_at = now

        from webinars_web.webinars import models as wm
        if self.event.account.is_webex:
            wm.StagedWebexRegistrant.post_stage(self.event)
        elif self.event.account.is_gtw:
            wm.StagedGTWRegistrant.post_stage(self.event)
        wm.StagedHubSpotRegistrant.post_stage(self.event)

        hashcodes = set()
        if self.event.account.is_webex:
            for m in [wm.StagedWebexRegistrant.objects, wm.StagedHubSpotRegistrant.objects, wm.WebexRegistrantSnapshot.objects, wm.HubSpotRegistrantSnapshot.objects, wm.Registrant.objects.filter(deleted_at__isnull=True)]:
                hashcodes |= set(m.filter(event=self.event).values_list('hashcode', flat=True))
        elif self.event.account.is_gtw:
            for m in [wm.StagedGTWRegistrant.objects, wm.StagedHubSpotRegistrant.objects, wm.GTWRegistrantSnapshot.objects, wm.HubSpotRegistrantSnapshot.objects, wm.Registrant.objects.filter(deleted_at__isnull=True)]:
                hashcodes |= set(m.filter(event=self.event).values_list('hashcode', flat=True))

        self.create_shards(wm.EventSyncShard, hashcodes, settings.EVENT_SHARD_SIZE)


    def possibly_sharded(self):
        if self.completed_at: return None
        if self.eventsyncshard_set.filter(completed_at__isnull=True).count(): return None

        now = time()
        locked = (self.__class__.objects.filter(id=self.id, sharded_at__isnull=True).update(sharded_at=now) == 1)
        if not locked: return None
        self.sharded_at = now

        self.completed_at = now
        self.save()
        self.event.post_sync_hook(self.started_at, self.completed_at)
        
        from django.db.models import Max
        for event_form in self.event.event_forms:
            max_last_modified_at = event_form.hubspoteventsyncstage_set.filter(parent_sync=self).aggregate(Max('finish_last_modified_at'))['finish_last_modified_at__max']
            if max_last_modified_at and max_last_modified_at > event_form.last_last_modified_at:
                event_form.last_last_modified_at = max_last_modified_at
                event_form.save()

        self.event.sync_finished()
        if self.parent:
            self.parent.possibly_done()

    #def force_shutdown(self):
        #self.forced_stop = True
        #self.completed_at = sanetime()
        #self.save()
        #self.event.current_sync = None
        #self.event.save()


    @property
    def kickoff_path(self):
        return "/webinars/event_syncs/%s/kickoff" % self.id
