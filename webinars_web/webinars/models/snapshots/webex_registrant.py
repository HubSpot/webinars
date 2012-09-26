from django.db import models
from sanetime.dj import SaneTimeField


class WebexRegistrantSnapshot(models.Model):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey('Event')
    hashcode = models.IntegerField(null=False)
    email = models.CharField(max_length=64, null=False)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    remote_id = models.CharField(max_length=128, null=True, editable=False)
    started_at = SaneTimeField(null=True)
    stopped_at = SaneTimeField(null=True)

    # unused
    ip_address = models.CharField(null=True,max_length=64)

