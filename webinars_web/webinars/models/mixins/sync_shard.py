from sanetime import time
from webinars_web.webinars.models.mixins import SyncParcel
from hapicrank.task_queues import Task
from utils.dict import merge


class SyncShard(SyncParcel):
    phase_type = 'shard'

    def go(self):
        if not self.lock_for_work(): return None
        self._sync()
        self.completed_at = time()
        self.save()
        self.parent_sync.possibly_sharded()

