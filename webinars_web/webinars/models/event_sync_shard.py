from django.db import models
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins
from sanetime import time


class EventSyncShard(models.Model, mixins.SyncShard):
    object_type = 'event'

    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    parent_sync = models.ForeignKey('EventSync')
    created_at = SaneTimeField(auto_now_add=True)
    started_at = SaneTimeField(null=True)
    completed_at = SaneTimeField(null=True)
    depth = models.IntegerField(null=False)
    section = models.IntegerField(null=False)
    size = models.IntegerField(null=False)

    @property
    def duration(self): 
        return ((self.completed_at or time()) - self.started_at).ms

    def _sync(self):
        self.parent_sync.event.sync_shard(self.depth, self.section)

