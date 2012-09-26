from django.db import models
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins


class StagedGTWRegistrant(models.Model, mixins.Staged):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey('Event')
    hashcode = models.IntegerField(null=False)
    email = models.CharField(max_length=64, null=False)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    key = models.CharField(max_length=128, null=True, editable=False)
    started_at = SaneTimeField(null=True)
    ended_at = SaneTimeField(null=True)
    duration = models.IntegerField(null=True) # in minutes

    @classmethod
    def fill(kls, event):
        from webinars_web.webinars import models as wm
        registrants = event.gtw_session.registrants
        with kls.delayed as d:
            for registrant in registrants:
                    raw_registrant = dict(
                        event_id = event.id,
                        email = registrant.email,
                        first_name = registrant.first_name,
                        last_name = registrant.last_name,
                        hashcode = wm.Registrant.calc_hashcode(registrant.email),
                        started_at = registrant.started_at and registrant.started_at.us,
                        ended_at = registrant.ended_at and registrant.ended_at.us,
                        duration = registrant.duration and registrant.duration.m,
                        key = str(registrant.key))
                    d.insert(raw_registrant)
            from django.db import transaction
            transaction.commit_unless_managed()
            return len(registrants)
