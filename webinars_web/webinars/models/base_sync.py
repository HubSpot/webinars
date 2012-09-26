from webinars_web.webinars.models import BaseContainerSync
from sanetime.dj import SaneTimeField
from sanetime import time
from hapicrank.task_queues import Task
from utils.dict import merge

class BaseSync(BaseContainerSync):
    class Meta:
        app_label = 'webinars'
        abstract = True

    staged_at = SaneTimeField(null=True)
    sharded_at = SaneTimeField(null=True)
    
    @property
    def staging_s(self): 
        return ((self.staged_at or time()) - self.started_at).fs

    @property
    def staging_ms(self): 
        return ((self.staged_at or time()) - self.started_at).fms

    @property
    def sharding_s(self): 
        return ((self.sharded_at or time()) - self.staged_at).fs

    @property
    def sharding_ms(self): 
        return ((self.sharded_at or time()) - self.staged_at).fms

    def _assemble_shard_dicts(self, hashcodes, shard_limit, depth, section):
        shard_dicts = []
        if len(hashcodes) <= shard_limit:
            shard_dicts.append(dict(parent_sync_id=self.id, depth=depth, size=len(hashcodes), section=section))
        else:
            shard_dicts.extend(self._assemble_shard_dicts([hc for hc in hashcodes if hc%(depth*2)==(section)], shard_limit, depth*2, section))
            shard_dicts.extend(self._assemble_shard_dicts([hc for hc in hashcodes if hc%(depth*2)==(section+depth)], shard_limit, depth*2, section+depth))
        return shard_dicts

    def create_shards(self, shard_kls, hashcodes, shard_limit):
        now = time()
        with shard_kls.delayed as d:
            for sd in self._assemble_shard_dicts(hashcodes, shard_limit, 1, 0):
                d.insert(merge(sd,dict(created_at=now.us)))
        from django.db import transaction
        transaction.commit_unless_managed()
        shards = shard_kls.objects.filter(parent_sync=self)
        if not self.debug: Task._enqueue([s.trigger_task for s in shards])
        return shards

