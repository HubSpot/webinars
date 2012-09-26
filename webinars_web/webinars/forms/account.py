from webinars_web.webinars.models import Account, AccountType
from webex.account import Account as WebexAccount
from webex.error import Error as WebexError
from django.forms import ModelForm, ValidationError

#import floppyforms as forms
from hsforms import fields, widgets
#from uni_form.helper import FormHelper
#from uni_form.layout import Layout, Div, ButtonHolder, Submit
from sanetime import time, delta

#from pprint import pprint


#FIELDS = ('account_type', 'username', 'password', 'extra_username', 'update_leads_on_unformed_events')

class AccountForm(ModelForm):
    class Meta:
        model = Account
        exclude = ('hub','prevent_unformed_lead_import','last_sync','current_sync','sync_lock','deleted_at', 'exclusion_date')

    #account_type = fields.TypedChoiceField(required=True, label='Provider', initial=AccountType.objects.get(pk=1), coerce=lambda idx: AccountType.objects.get(pk=idx))
    username = fields.CharField(label='Username', required=True)
    password = fields.CharField(label="Password", required=True, widget=widgets.PasswordInput(render_value=True))
    extra = fields.CharField(label="Webex Domain", required=True, attrs={})

    exclude_old_events_from_hubspot = fields.BooleanField(label="Historical Sync Options", required=False, widget=widgets.RadioSelect())
    exclusion_date_delta = fields.ChoiceField(label="Exclusion Date Delta", required=True, attrs={'class':'medium'}, choices=((0,'Now'), (30,'One Month'), (90,'90 Days')))
#    prevent_unformed_lead_import = fields.BooleanField(label="", required=False)


    def __init__(self, *args, **kwargs):
        self.hub = kwargs.pop('hub')
        super(AccountForm,self).__init__(*args, **kwargs)
        self.current_account_type_id = kwargs.get('instance') and kwargs['instance'].account_type.id or 2
        self.account_type_infos = [(at.id, at.name, at.is_available(self.hub),at.image_name) for at in AccountType.objects.all().order_by('id')]
        d = dict((ati[1], ati) for ati in self.account_type_infos)
        self.account_type_infos = [d[name] for name in ('GoToWebinar','Webex Event Center', 'GoToMeeting', 'Webex Meeting Center', 'ReadyTalk', 'Infinite')]


    def clean(self):
        if self._errors.keys(): return self.cleaned_data
        if self.cleaned_data['account_type'].id == 1:
            site_name = self.cleaned_data['extra']
            site_name = (site_name.split('://')+[''])[-2].split('.')[0]
            self.cleaned_data['extra'] = site_name
            kwargs = dict(
                username = self.cleaned_data['username'],
                password = self.cleaned_data['password'],
                site_name = site_name)
            webex_account = WebexAccount(**kwargs)
            try:
                version = webex_account.version
            except WebexError:
                raise ValidationError("This Webex Domain is not valid.  Please correct your Webex Domain.")
            if version < 5.9:
                raise ValidationError("The Webinars App only works with the most recent version of the Webex API (5.9).  Your account is using the %s version of the API.  Your CSM at Webex can help you upgrade your Webex version." % (version))
            try:
                webex_account.site_instance
            except WebexError as err:
                raise ValidationError("Webex does not recognize these as valid credentials!  Webex Response: %s"%err)
            if Account.objects.filter(hub=self.hub, username=kwargs['username'], extra=site_name, deleted_at__isnull=True):
                raise ValidationError("An account with this username and domain name has already been connected.  If you need to amend something about this account go to the 'Accounts' page and then 'edit' the account.")
        return self.cleaned_data
