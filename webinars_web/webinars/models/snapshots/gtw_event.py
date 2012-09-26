from django.db import models as djmodels
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins


#TODO: make sure we enforce webex limits on names everywhere we need to so we don't create sync thrashing

class GTWEventSnapshot(djmodels.Model, mixins.Event):
    class Meta:  # needed cuz we've broken out models.py into a models package
        app_label = 'webinars'

    account = djmodels.ForeignKey('Account')
    hashcode = djmodels.IntegerField(null=False)
    remote_id = djmodels.CharField(max_length=128, null=False)
    alt_remote_id = djmodels.CharField(max_length=128, null=True)
    title = djmodels.CharField(max_length=256, null=False)
    description = djmodels.CharField(max_length=2**14-1, null=True)

    _time_starts_at = SaneTimeField(null=True)
    _time_ends_at = SaneTimeField(null=True)
    _time_started_at = SaneTimeField(null=True)
    _time_ended_at = SaneTimeField(null=True)
    _timezone = djmodels.CharField(max_length=64, null=True, editable=False)


