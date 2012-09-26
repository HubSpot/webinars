from django.db import models
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import Event, CmsForm

class EventForm(models.Model):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey(Event)
    cms_form = models.ForeignKey(CmsForm)
    last_last_modified_at = SaneTimeField(null=False, default=0)
    converted_at_cutoff = SaneTimeField(null=False, default=0)

