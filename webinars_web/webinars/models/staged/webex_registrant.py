from django.db import models
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins


class StagedWebexRegistrant(models.Model, mixins.Staged):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey('Event')
    hashcode = models.IntegerField(null=False)
    email = models.CharField(max_length=64, null=False)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    attendee_id = models.CharField(max_length=128, null=True, editable=False)
    started_at = SaneTimeField(null=True)
    stopped_at = SaneTimeField(null=True)

    # unused
    duration = models.IntegerField(null=True) # in minutes
    ip_address = models.CharField(null=True,max_length=64)

    @classmethod
    def fill(kls, event):
        from webinars_web.webinars import models as wm
        # webex allows registrants with no email to be created. I don't!
        registrants = filter(lambda x: x.email, event.webex_event.registrants)
        with kls.delayed as d:
            for registrant in registrants:
                    raw_registrant = dict(
                        event_id = event.id,
                        email = registrant.email,
                        first_name = registrant.first_name,
                        last_name = registrant.last_name,
                        hashcode = wm.Registrant.calc_hashcode(registrant.email),
                        started_at = registrant.started_at and registrant.started_at.us,
                        stopped_at = registrant.stopped_at and registrant.stopped_at.us,
                        attendee_id = registrant.attendee_id)
                    d.insert(raw_registrant)
            from django.db import transaction
            transaction.commit_unless_managed()
            return len(registrants)
