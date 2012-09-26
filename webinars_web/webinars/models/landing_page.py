from django.db import models
from webinars_web.webinars.models.cms_form import CmsForm
#from pprint import pprint

class LandingPage(models.Model):
    class Meta:
        app_label = 'webinars'

    cms_form = models.ForeignKey(CmsForm, null=False) # should this be False?
    form_title = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=128)

    def __unicode__(self):
        return "%s / %s" % (self.self.name, self.form_title)


