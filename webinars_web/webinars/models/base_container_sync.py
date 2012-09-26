from django.db import models as djmodels
from sanetime.dj import SaneTimeField
from sanetime import time,delta

class BaseContainerSync(djmodels.Model):
    class Meta:
        app_label = 'webinars'
        abstract = True

    completed_at = SaneTimeField(null=True)
    forced_stop = djmodels.BooleanField(null=False, default=False)
    visible = djmodels.BooleanField(null=False, default=False)
    debug = djmodels.BooleanField(null=False, default=False)
    error = djmodels.CharField(max_length=4096, null=True)
    
    @property
    def s(self): 
        return ((self.completed_at or time()) - self.started_at).fs

    @property
    def delta(self): return (self.completed_at or time()) - self.started_at

    @property
    def is_worrisome(self): return not self.completed_at and (time() - self.started_at) > delta(m=10)
    @property
    def is_bad(self): return not self.completed_at and (time() - self.started_at) > delta(h=1)

    @property
    def ms(self): 
        return ((self.completed_at or time()) - self.started_at).fms

