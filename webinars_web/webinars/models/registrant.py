from django.db import models
from webinars_web.webinars.models.event import Event
from webinars_web.webinars.models.cms_form import CmsForm
from sanetime.dj import SaneTimeField
from sanetime import time
import hashlib
from django.conf import settings


class Registrant(models.Model):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey(Event)
    hashcode = models.IntegerField(null=False)
    remote_id = models.CharField(max_length=128, null=True, editable=False)
    lead_guid = models.CharField(null=True, max_length=36)
    email = models.CharField(max_length=64)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)

    cms_form = models.ForeignKey(CmsForm, null=True)
    started_at = SaneTimeField(null=True)
    stopped_at = SaneTimeField(null=True)

    updated_at = SaneTimeField(auto_now=True)
    created_at = SaneTimeField(auto_now_add=True)
    deleted_at = SaneTimeField(null=True, editable=False)

    # unused
    ip_address = models.CharField(null=True,max_length=64)


    @property
    def initial_form_guid(self): return self.cms_form_guid

    @initial_form_guid.setter
    def initial_form_guid(self, guid): 
        self.cms_form = CmsForm.objects.get(pk=guid)

    @property
    def effective_started_at(self):
        return self.started_at and (self.started_at < self.event.starts_at and self.event.starts_at or self.started_at)

    @property
    def effective_stopped_at(self):
        return self.stopped_at and (self.stopped_at > self.event.ends_at and self.event.ends_at or self.stopped_at)

    @property
    def effective_duration(self):
        return self.effective_started_at and self.effective_stopped_at and (self.effective_stopped_at - self.effective_started_at)

    @property
    def registered_any(self): return True

    @property
    def registered_this(self): return True

    @property
    def attended_any(self): return self.duration and True or None

    @property
    def attended_this(self):
        if self.duration: return True
        if self.event._ended_at and time() > self.event._ended_at: return False
        return None

    @classmethod
    def calc_hashcode(kls, email):
        return int(int(hashlib.md5(email).hexdigest(),16)%2**31)

    def ensure_hashcode(self):
        self.hashcode = self.__class__.calc_hashcode(self.email)

    @property
    def caring_percentage(self): return int(self.duration)*100.0 / int(self.event.caring_duration)

    @property
    def caring_start_percentage(self): return int(self.started_at - self.event.start_caring_at)*100.0 / int(self.event.caring_duration)

    @property
    def duration(self):
        return self.stopped_at and self.started_at and self.stopped_at-self.started_at

    @property
    def present_at_starts_at(self): return self.started_at and self.stopped_at and self.started_at <= self.event.starts_at and self.stopped_at >= self.event.starts_at
    @property
    def present_at_ends_at(self): return self.started_at and self.stopped_at and self.started_at <= self.event.ends_at and self.stopped_at >= self.event.ends_at

    @property
    def lead_url(self): return "https://%s/leads/app/lead?portalId=%s&guid=%s" %( settings.APP_DOMAIN, self.event.account.hub.id, self.lead_guid ) if self.lead_guid else None

