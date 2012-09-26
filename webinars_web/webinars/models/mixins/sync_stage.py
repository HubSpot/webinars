from sanetime import time
from webinars_web.webinars.models.mixins import SyncParcel


class SyncStage(SyncParcel):
    phase_type = 'stage'
    #error = djmodels.CharField(max_length=4096, null=True)

    def go(self):
        if not self.lock_for_work(): return None
        #TODO: need to generalize for sharding side as well-- and do i put errors in dB or no?  just logs?
        try:
            size, new_stages = self._fill()
        except:
            import traceback
            error = traceback.format_exc()
            self.open_for_rework()
            raise Exception(error)
        self.size = size
        self.completed_at = time()
        self.save()
        if not new_stages:
            self.parent_sync.possibly_staged()

