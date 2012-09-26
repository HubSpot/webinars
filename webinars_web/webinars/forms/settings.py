from django import forms
#from pprint import pprint


class SettingsForm(forms.Form):
    avoid_sync = forms.BooleanField(required=True)

