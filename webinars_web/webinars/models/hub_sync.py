from django.db import models
from sanetime import time
from webinars_web.webinars.models import BaseContainerSync
from sanetime.dj import SaneTimeField

class HubSync(BaseContainerSync):
    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    started_at = SaneTimeField(auto_now_add=True)
    hub = models.ForeignKey('Hub', null=False)

    @property
    def account_syncs(self):
        return self.accountsync_set.all().order_by('-account__created_at')

    def start(self):
        for account in self.hub.account_set.filter(current_sync__isnull=True, deleted_at__isnull=True):
            account.sync(force=False, visible=self.visible, debug=self.debug, parent_sync=self)
        self.possibly_done()
        return self

    def possibly_done(self):
        if self.completed_at: return None
        if self.accountsync_set.filter(completed_at__isnull=True).count() == 0:
            now = time()
            if self.__class__.objects.filter(id=self.id, completed_at__isnull=True).update(completed_at=now) == 1:
                self.completed_at = now
                self.hub.sync_finished()

    def _get_account_syncs(self):
        return self.accountsync_set.all()
    account_syncs = property(_get_account_syncs)

    def progress(self):
        pass #TODO

