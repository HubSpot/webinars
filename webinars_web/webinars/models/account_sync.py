from django.db import models
from django.conf import settings
from sanetime import time
from webinars_web.webinars.models import BaseSync
from hapicrank.task_queues import Task
from sanetime.dj import SaneTimeField
from utils.property import cached_property
import logging

class AccountSync(BaseSync):
    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    started_at = SaneTimeField(auto_now_add=True)
    parent = models.ForeignKey('HubSync', null=True)
    account = models.ForeignKey('Account', null=False)

    @cached_property
    def stages(self): return self.accountsyncstage_set.all().order_by('offset')

    @cached_property
    def shards(self): return self.accountsyncshard_set.all()

    @cached_property
    def event_syncs(self): return self.eventsync_set.all()

    def start(self):
        from webinars_web.webinars import models as wm
        if self.account.is_webex:
            wm.StagedWebexEvent.pre_stage(self.account)
        elif self.account.is_gtw:
            wm.StagedGTWEvent.pre_stage(self.account)
        wm.AccountSyncStage.trigger_initial_stages(self)
        return self

    def possibly_staged(self):
        if self.completed_at: return None
        if self.accountsyncstage_set.filter(completed_at__isnull=True).count(): return None

        now = time()
        locked = (self.__class__.objects.filter(id=self.id, staged_at__isnull=True).update(staged_at=now) == 1)
        if not locked: return None
        self.staged_at = now

        from webinars_web.webinars import models as wm
        if self.account.is_webex:
            wm.StagedWebexEvent.post_stage(self.account)
        if self.account.is_gtw:
            wm.StagedGTWEvent.post_stage(self.account)

        hashcodes = set()
        if self.account.account_type.name.lower() == 'webex':
            for m in [wm.StagedWebexEvent.objects, wm.WebexEventSnapshot.objects, wm.Event.objects.filter(deleted_at__isnull=True)]:
                hashcodes |= set(m.filter(account=self.account).values_list('hashcode', flat=True))
        elif self.account.account_type.name.lower() == 'gotowebinar':
            for m in [wm.StagedGTWEvent.objects, wm.GTWEventSnapshot.objects, wm.Event.objects.filter(deleted_at__isnull=True)]:
                hashcodes |= set(m.filter(account=self.account).values_list('hashcode', flat=True))

        self.create_shards(wm.AccountSyncShard, hashcodes, settings.ACCOUNT_SYNC_SHARD_SIZE)

    def possibly_sharded(self):
        if self.completed_at: return None
        if self.accountsyncshard_set.filter(completed_at__isnull=True).count(): return None

        now = time()
        locked = (self.__class__.objects.filter(id=self.id, sharded_at__isnull=True).update(sharded_at=now) == 1)
        if not locked: return None
        self.sharded_at = now

        from webinars_web.webinars import models as wm
        with wm.EventSync.delayed as d:
            now = time()
            for event in self.account.event_set.filter(deleted_at__isnull=True, current_sync__isnull=True, mothballed=False).select_related('account'):
                d.insert(dict(event_id=event.id, parent_id=self.id, visible=self.visible, debug=self.debug, created_at=now.us))
        from django.db import transaction
        transaction.commit_unless_managed()
        event_syncs = wm.EventSync.objects.filter(parent=self, event__account=self.account)
        if not self.debug:
            tasks = []
            for es in event_syncs:
                url = '%s%s'%(settings.APP_URL,es.kickoff_path)
                uid = 'event_sync|kickoff|%s'%es.id
                qid = es.event.account_id % settings.NUM_QUEUES
                logging.debug('TQDEBUG: qid id %s' % qid)
                tasks.append(Task(queue=settings.TASK_QUEUES[qid], url=url, method='POST', uid=uid))
            Task._enqueue(tasks)
            
        self.possibly_done()

    def possibly_done(self):
        
        if self.completed_at: return None
        if self.eventsync_set.filter(completed_at__isnull=True).count() == 0:
            now = time()
            if self.__class__.objects.filter(id=self.id, completed_at__isnull=True).update(completed_at=now) == 1:
                self.completed_at = now
                self.account.sync_finished()
                if self.parent:
                    self.parent.possibly_done()

