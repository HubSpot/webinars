from django.db import models
from sanetime.dj import SaneTimeField


class HubSpotRegistrantSnapshot(models.Model):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey('Event')
    hashcode = models.IntegerField(null=False)
    email = models.CharField(max_length=64, null=False)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    lead_guid = models.CharField(null=True, max_length=36)
    initial_form_guid = models.CharField(null=True, max_length=36)
    registered_any = models.NullBooleanField(null=True)
    registered_this = models.NullBooleanField(null=True)
    attended_any = models.NullBooleanField(null=True)
    attended_this = models.NullBooleanField(null=True)
    started_at = SaneTimeField(null=True)
    stopped_at = SaneTimeField(null=True)

