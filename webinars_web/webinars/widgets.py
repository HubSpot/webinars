from django.forms import widgets
from sanetime import time

class SplitSaneTimeWidget(widgets.SplitDateTimeWidget):
    def __init__(self, *args, **kwargs):
        self.tz = kwargs.pop('tz', None)
        super(SplitSaneTimeWidget, self).__init__(*args, **kwargs)

    def decompress(self, value):
        if value:
            value = time(int(value), self.tz).to_naive_datetime()
        return super(SplitSaneTimeWidget, self).decompress(value)

class BootstrapCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul class="inputs-list">']
        # Normalize to strings
        str_values = set([widgets.force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(widgets.chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))

            cb = widgets.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = widgets.force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = widgets.force_unicode(option_label)  # purposefully did not escape so I can get html in here
            output.append(u'<li><label>%s<span>%s</span></label></li>' % (rendered_cb, option_label))
        output.append(u'</ul>')
        return widgets.mark_safe(u'\n'.join(output))


