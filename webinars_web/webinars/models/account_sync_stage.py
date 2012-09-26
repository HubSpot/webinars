from django.db import models
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins
from sanetime import time


class AccountSyncStage(models.Model, mixins.SyncStage):
    object_type = 'account'

    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    parent_sync = models.ForeignKey('AccountSync')
    created_at = SaneTimeField(auto_now_add=True)
    started_at = SaneTimeField(null=True)
    completed_at = SaneTimeField(null=True)
    size = models.IntegerField(null=True)

#unused
    offset = models.IntegerField(null=False)
    max_size = models.IntegerField(null=False)
    last = models.BooleanField(null=False, default=False)
    historical = models.BooleanField(null=False, default=False)

    @property
    def duration(self): 
        return ((self.completed_at or time()) - self.started_at).ms

    def _fill(self):
        from webinars_web.webinars import models as wm
        new_stages = []
        account = self.parent_sync.account
        if account.is_webex:
            size = wm.StagedWebexEvent.fill(account=account)
        elif account.is_gtw:
            size = wm.StagedGTWEvent.fill(account=account)
        return (size, new_stages)

    @classmethod
    def trigger_initial_stages(kls, account_sync):
        stages = []
        stage = kls.objects.create(parent_sync=account_sync, offset=0, max_size=0, last=True).trigger()
        stages.append(stage)
        return stages

