from django.db import models
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins
from sanetime import time


class HubSpotEventSyncStage(models.Model, mixins.SyncStage):
    object_type = 'event'
    phase_type = 'hubspot_stage'

    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    parent_sync = models.ForeignKey('EventSync')
    created_at = SaneTimeField(auto_now_add=True)
    started_at = SaneTimeField(null=True)
    completed_at = SaneTimeField(null=True)
    offset = models.IntegerField(null=False, default=0)
    start_last_modified_at = SaneTimeField(null=False)
    event_form = models.ForeignKey('EventForm')
    max_size = models.IntegerField(null=False)
    size = models.IntegerField(null=True)
    finish_last_modified_at = SaneTimeField(null=True)

    @property
    def duration(self): 
        return ((self.completed_at or time()) - self.started_at).ms

    @property
    def last(self): 
        return True

    @property
    def start_last_modified_at_snippet(self):
        return self.start_last_modified_at.ms % 1000

    def _fill(self):
        from webinars_web.webinars import models as wm
        new_stages = []
        (size, finish_last_modified_at) = wm.StagedHubSpotRegistrant.fill(event=self.parent_sync.event, offset=self.offset, start_last_modified_at=self.start_last_modified_at, max_size=self.max_size, event_form=self.event_form)
        self.finish_last_modified_at = finish_last_modified_at
        if size>=self.max_size:
            new_stages = [self._create_next_stage().trigger()]
        return (size, new_stages)

    def _create_next_stage(self):
        offset = 0
        start_last_modified_at = self.finish_last_modified_at
        if start_last_modified_at == self.start_last_modified_at:
            overlap = int(self.max_size**0.39-1)
            offset = self.offset+self.max_size-overlap
        return self.__class__.objects.create(parent_sync=self.parent_sync, offset=offset, start_last_modified_at=start_last_modified_at, max_size=self.max_size, event_form=self.event_form)

