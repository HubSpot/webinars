from django import forms
from django.conf import settings
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe
from django.forms import ValidationError
from webinars_web.webinars import models as wm

from sanetime import time
from hsforms import fields as hsfields
from hsforms import widgets as hswidgets


class BootstrapErrorList(ErrorList):
    def __unicode__(self):
        return self.as_csv()

    def as_csv(self):
        if not self: return u''
        return u', '.join([e for e in self])

class CmsFormMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        s = '<span class="form-name">%s</span>' % obj.name
        s += '<span class="lps">'
        for lp in self.lp_hash[obj.guid]:
            s+= '<a href="%s" title="%s" target="_blank"><img src="http://%s/final/img/common/icons/external_link.gif"/></a>' % (lp.url, lp.name, settings.STATIC_DOMAIN)
        s += '</span>'
        return mark_safe(s)

    @property
    def lp_hash(self):
        if getattr(self,'_lp_hash',None) == None:
            self._lp_hash = {}
            for lp in wm.LandingPage.objects.filter(cms_form__hub = self.hub):
                self._lp_hash.setdefault(lp.cms_form_id, []).append(lp)
        return self._lp_hash

TRUERB = mark_safe('Register <strong>all</strong> leads from the selected forms')
FALSERB = mark_safe('Register <strong>only</strong> leads <strong>since</strong> form association')


class EventForm(forms.ModelForm):

    class Meta:
        model = wm.Event
        fields = ( 'account', 'title', 'starts_at_ndt', 'duration', 'description', 'cms_forms', 'sync_leads_for_all_time')

    account = hsfields.TypedChoiceField(required=True, label='Provider', coerce=lambda idx: wm.Account.objects.get(pk=idx))
    title = hsfields.CharField(label="Title", required=True, attrs={'class':'xlarge'})
    starts_at_ndt = hsfields.SplitDateTimeField(label='Date & Time', required=True)
    duration = hsfields.ChoiceField(label="Duration", required=True, attrs={'class':'medium'}, choices=((15,'15 minutes'),(30,'30 minutes'),(45,'45 minutes'),(60,'1 hour'),(90,'1.5 hour'),(120,'2 hour'),(150,'2.5 hour'),(180,'3 hour')))
    description = hsfields.CharField(label="Description", required=True, widget=hswidgets.FlexibleTextareaInput(), attrs={'class':'xlarge'})  #FIXME: need to get xlarge into the widget somehow! ughhh 
    cms_forms = CmsFormMultipleChoiceField(None, label="HubSpot Forms", widget=hswidgets.CheckboxSelectMultiple(), required=False)
    sync_leads_for_all_time = hsfields.BooleanField(label="Association Options", required=False, widget=hswidgets.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.hub = kwargs.pop('hub')
        kwargs['error_class'] = BootstrapErrorList
        super(EventForm, self).__init__(*args, **kwargs)
        self.hidden_inputs = {}
        self.kwargs_instance = kwargs.get('instance')
        self.fields['cms_forms'].hub = self.hub
        self.fields['cms_forms'].queryset = wm.CmsForm.objects.filter(hub = self.hub, is_sync_target=False).order_by('name')
        self.fields['account'].choices = [(a.id, a.identifier) for a in wm.Account.objects.filter(hub=self.hub, deleted_at__isnull=True)]
        if len(self.fields['account'].choices) <=1 and not (self.kwargs_instance and not self.kwargs_instance.editable_details):
            self.fields['account'].widget.attrs['readonly'] = 'readonly'
        self.fields['sync_leads_for_all_time'].widget.choices = ((False,FALSERB), (True,TRUERB)) 
        #self.fields['sync_leads_for_all_time'].widget.choices = ((False,FALSERB % self.kwargs_instance and self.kwargs_instance.created_at.strftime('%b %d %I:%M%p') or sanetime().strftime('%b %d %I:%M%p'), (True,TRUERB)) 
        if kwargs.get('instance'):
            self.fields['starts_at_ndt'].initial = self.instance.starts_at.ndt
            self.fields['starts_at_ndt'].help_text = "%s Timezone" % self.instance.starts_at.tz
            self.fields['duration'].initial = self.instance.duration.m
        else:
            self.fields['starts_at_ndt'].help_text = "%s Timezone" % self.hub.timezone
            self.fields['duration'].initial = 60
            self.fields['sync_leads_for_all_time'].initial = False
        if self.kwargs_instance and not self.kwargs_instance.editable_details:
            self.fields['account'].widget.attrs['readonly'] = 'readonly'
            self.fields['title'].widget.attrs['readonly'] = 'readonly'
            self.fields['starts_at_ndt'].widget.attrs['readonly'] = 'readonly'
            self.fields['duration'].widget.attrs['readonly'] = 'readonly'
            self.fields['description'].widget.attrs['readonly'] = 'readonly'
#            self.fields['description'].required = False

    def clean_starts_at_ndt(self):
        if not self.kwargs_instance or not self.kwargs_instance.account.is_gtw:
            tz = self.kwargs_instance and self.kwargs_instance.starts_at.tz or self.hub.timezone
            st = time(self.cleaned_data['starts_at_ndt'], tz)
            if time() > st:
                raise ValidationError("This is in the past!")
        return self.cleaned_data['starts_at_ndt']

    

