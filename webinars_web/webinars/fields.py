from django import forms
from sanetime import time
from webinars_web.webinars.widgets import SplitSaneTimeWidget

class SplitSaneTimeField(forms.SplitDateTimeField):
    widget = SplitSaneTimeWidget
    #hidden_widget = SplitHiddenDateTimeWidget
    #default_error_messages = {
        #'invalid_date': _(u'Enter a valid date.'),
        #'invalid_time': _(u'Enter a valid time.'),
    #}

    def __init__(self, *args, **kwargs):
        self.tz = kwargs.pop('tz', None)
        super(SplitSaneTimeField, self).__init__(*args, **kwargs)

    def compress(self, data_list):
        st = None
        dt = super(SplitSaneTimeField, self).compress(data_list)
        if dt is not None:
            st = time(dt, self.tz)
        return st


class SplitSaneTzTimeField(forms.SplitDateTimeField):
    widget = SplitSaneTimeWidget
    #hidden_widget = SplitHiddenDateTimeWidget
    #default_error_messages = {
        #'invalid_date': _(u'Enter a valid date.'),
        #'invalid_time': _(u'Enter a valid time.'),
    #}

    def __init__(self, *args, **kwargs):
        self.tz = kwargs.pop('tz', None)
        super(SplitSaneTzTimeField, self).__init__(*args, **kwargs)

    def compress(self, data_list):
        st = None
        dt = super(SplitSaneTzTimeField, self).compress(data_list)
        if dt is not None:
            st = time(dt, self.tz)
        return st

