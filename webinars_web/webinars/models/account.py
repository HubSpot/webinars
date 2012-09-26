from django.db import models
from webinars_web.webinars.models import AccountType, Hub
from sanetime.dj import SaneTimeField
from webex.account import Account as WebexAccount
from gtw import Organizer as GTWOrganizer
from webinars_web.webinars.models import mixins
from sanetime import time
from utils.property import cached_property
import logging

class Account(models.Model, mixins.Trigger):
    class Meta:
        app_label = 'webinars'

    account_type = models.ForeignKey(AccountType)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    extra = models.CharField(max_length=64, null=True)
    hub = models.ForeignKey(Hub)
    prevent_unformed_lead_import = models.BooleanField(default=False)
    default = models.BooleanField(null=False,default=False)
#    version = models.CharField(max_length=32, null=True)

    updated_at = SaneTimeField(auto_now=True)
    created_at = SaneTimeField(auto_now_add=True)
    deleted_at = SaneTimeField(null=True)
    
    exclude_old_events_from_hubspot = models.BooleanField(null=False, default=False)
    exclusion_date = SaneTimeField(null=True)

    last_sync = models.ForeignKey('AccountSync', null=True, related_name='+')
    current_sync = models.ForeignKey('AccountSync', null=True, related_name='+')
    sync_lock = models.CharField(max_length=36, null=True)

    def sync(self, force=False, visible=False, debug=False, parent_sync=None):
        from webinars_web.webinars import models as wm
        if force: self.shutdown_all_syncs()
        if not self._lock_for_sync(): 
            if visible and self.current_sync and not self.current_sync.visible:
                wm.AccountSync.objects.filter(id=self.current_sync.id).update(visible=visible)
            return None
        account_sync = wm.AccountSync.objects.create(account=self, visible=visible, debug=debug, parent=parent_sync)
        self.current_sync = account_sync
        self.save()
        logging.debug('sync started for %s'%self.hub)
        return account_sync.start()

    def shutdown_all_syncs(self):
        from webinars_web.webinars import models as wm
        now = time()
        wm.AccountSync.objects.filter(completed_at__isnull=True, account=self).update(completed_at=now, forced_stop=True)
        wm.AccountSyncStage.objects.filter(completed_at__isnull=True, parent_sync__account=self).update(completed_at=now)
        wm.AccountSyncShard.objects.filter(completed_at__isnull=True, parent_sync__account=self).update(completed_at=now)

        #event specific #TODO: dry up better with the event version of this)
        wm.EventSync.objects.filter(completed_at__isnull=True, event__account=self).update(completed_at=now, forced_stop=True)
        wm.GTWEventSyncStage.objects.filter(completed_at__isnull=True, parent_sync__event__account=self).update(completed_at=now)
        wm.WebexEventSyncStage.objects.filter(completed_at__isnull=True, parent_sync__event__account=self).update(completed_at=now)
        wm.HubSpotEventSyncStage.objects.filter(completed_at__isnull=True, parent_sync__event__account=self).update(completed_at=now)
        wm.EventSyncShard.objects.filter(completed_at__isnull=True, parent_sync__event__account=self).update(completed_at=now)

        wm.Event.objects.filter(account=self).update(current_sync=None, sync_lock=None)
        if self.current_sync or self.sync_lock:
            self.__class__.objects.filter(pk=self.id).update(current_sync=None, sync_lock=None)
            self.current_sync = self.sync_lock = None

    def __unicode__(self):
        return "%s: %s" % (self.account_type.name, self.username)

    @property
    def webex_account(self):
        return WebexAccount(username=self.username, password=self.password, site_name=self.extra)

    @property
    def gtw_organizer(self):
        return GTWOrganizer(organizer_key=self.username, oauth_token=self.password)

    @property
    def is_webex(self): return self.account_type_id==1
    @property
    def is_gtw(self): return self.account_type_id==2

    @property
    def identifier(self):
        if self.is_webex:
            return "%s / %s" % (self.username, self.extra)
        elif self.is_gtw:
            return "%s (%s)" % (self.extra, self.username)
        return "?"



    def sync_shard(self, depth, section):
        if self.is_webex:
            from webinars_web.webinars.cynq.event import EventLocalStore, WebexEventSnapshotStore
            from webinars_web.webinars.cynq.event import WebexEventSpec, WebexEventRemoteStore
            from cynq import Controller, Arm
            spec = WebexEventSpec()
            local = EventLocalStore(self, depth, section)
            snapshot = WebexEventSnapshotStore(self, depth, section)
            api = WebexEventRemoteStore(self, depth, section)
            arm = Arm(spec, api, local, snapshot)
            return Controller(arm).cynq()
        elif self.is_gtw:
            from webinars_web.webinars.cynq.event import EventLocalStore, GTWEventSnapshotStore
            from webinars_web.webinars.cynq.event import GTWEventSpec, GTWEventRemoteStore
            from cynq import Controller, Arm
            spec = GTWEventSpec()
            local = EventLocalStore(self, depth, section)
            snapshot = GTWEventSnapshotStore(self, depth, section)
            api = GTWEventRemoteStore(self, depth, section)
            arm = Arm(spec, api, local, snapshot)
            return Controller(arm).cynq()

    def expunge(self):
        from django.db import connection, transaction
        cursor = connection.cursor()

        cursor.execute('UPDATE webinars_hub SET last_sync_id=NULL, current_sync_id=NULL, sync_lock=NULL WHERE id=%s', [self.hub_id])
        cursor.execute('UPDATE webinars_account SET last_sync_id=NULL, current_sync_id=NULL, sync_lock=NULL WHERE id=%s', [self.id])
        cursor.execute('UPDATE webinars_event SET last_sync_id=NULL, current_sync_id=NULL, sync_lock=NULL WHERE account_id=%s', [self.id])

        cursor.execute('DELETE FROM webinars_gtweventsyncstage WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_webexeventsyncstage WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_hubspoteventsyncstage WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_eventsyncshard WHERE parent_sync_id IN (SELECT DISTINCT es.id FROM webinars_eventsync es JOIN webinars_event e ON e.id = es.event_id WHERE e.account_id=%s)', [self.id])

        cursor.execute('DELETE FROM webinars_eventsync WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])

        cursor.execute('DELETE FROM webinars_accountsyncstage WHERE parent_sync_id IN (SELECT id FROM webinars_accountsync WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_accountsyncshard WHERE parent_sync_id IN (SELECT id FROM webinars_accountsync WHERE account_id=%s)', [self.id])

        cursor.execute('DELETE FROM webinars_registrant WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_gtwregistrantsnapshot WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_webexregistrantsnapshot WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_hubspotregistrantsnapshot WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_stagedgtwregistrant WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_stagedwebexregistrant WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])
        cursor.execute('DELETE FROM webinars_stagedhubspotregistrant WHERE event_id IN (SELECT id FROM webinars_event WHERE account_id=%s)', [self.id])

        cursor.execute('DELETE FROM webinars_event WHERE account_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_webexeventsnapshot WHERE account_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_stagedwebexevent WHERE account_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_gtweventsnapshot WHERE account_id=%s', [self.id])
        cursor.execute('DELETE FROM webinars_stagedgtwevent WHERE account_id=%s', [self.id])

        cursor.execute('DELETE FROM webinars_accountsync WHERE account_id=%s', [self.id])

        cursor.execute('DELETE FROM webinars_account WHERE id=%s', [self.id])

        transaction.commit_unless_managed()



    @cached_property
    def events(self): return self.event_set.all()


