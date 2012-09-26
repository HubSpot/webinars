from uuid import uuid4

class Trigger(object):

    def __init__(self):
        super(Trigger, self).__init__()

    def _lock_for_sync(self):
        lock = str(uuid4())
        locked = self.__class__.objects.filter(id=self.id, sync_lock__isnull=True).update(sync_lock=lock) == 1
        if locked:
            self.sync_lock = lock  # the update wouldn't have updated self-- so I'm just making it consistent here
        return locked

    def sync_finished(self):
        self.__class__.objects.filter(pk=self.id).update(last_sync=self.current_sync,current_sync=None,sync_lock=None)
        self.last_sync = self.current_sync
        self.current_sync = None
        self.sync_lock = None

    def ensure_sync(self, visible=False):
        sync = self.sync(visible=visible) or self.current_sync
        if visible and not sync.visible:  # make current sync visible if we're trying to kick off a visible one and there's a non-visible one already going
            sync.visible = True
            sync.save()
        return sync

