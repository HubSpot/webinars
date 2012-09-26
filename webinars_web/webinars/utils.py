from django import forms

def partition(iterable, func, ensure_keys=None):
    result = {}
    if ensure_keys:
        for k in ensure_keys:
            result[k] = []
    for i in iterable:
        result.setdefault(func(i), []).append(i) 
    return result


# refactor into more general utility!
def as_bootstrap(form, fieldset=None, fields=None, hidden=False):
    top_errors = form.non_field_errors() # Errors that should be displayed above all fields.
    output, hidden_fields = [], []

    if fieldset:
        output.append(u'<legend>%s</legend>'%fieldset)

    for name, field in form.fields.items():
        if hidden or name in fields:
            bf = forms.forms.BoundField(form, field, name)
            bf_errors = form.error_class([forms.forms.conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden and hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, forms.forms.force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            elif name in fields:
                error_row = u'<div class="clearfix"></div>'
                if bf.label:
                    label = forms.forms.conditional_escape(forms.forms.force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if form.label_suffix:
                        if label[-1] not in ':?.!':
                            label += form.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''
                help_text_html = u'\n<span class="help-inline">%s</span>'
                if bf_errors:
                    help_text = help_text_html % forms.forms.force_unicode(bf_errors)
                elif field.help_text:
                    help_text = help_text_html % forms.forms.force_unicode(field.help_text)
                else:
                    help_text = u''
                outer_classes = ['clearfix']
                if bf_errors:
                    outer_classes.append('error')
                inner_classes = ['input']
                html_classes = bf.css_classes()
                if html_classes:
                    inner_classes.extend(html_classes.split(' '))
                normal_row = u'''
<div class="%(outer_classes)s">
%(label)s
<div class="%(inner_classes)s">
    %(field)s%(help_text)s
</div>
</div>
                '''

                output.append(normal_row % {
                    'outer_classes': forms.forms.force_unicode(' '.join(outer_classes)),
                    'inner_classes': forms.forms.force_unicode(' '.join(inner_classes)),
                    'label': forms.forms.force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text
                })

    if hidden and top_errors:
        output.insert(0, error_row % forms.forms.force_unicode(top_errors))

    if hidden and hidden_fields: # Insert any hidden fields in the last row.
        output.insert(0, u''.join(hidden_fields))

    return forms.forms.mark_safe(u'<fieldset>%s</fieldset>'%u'\n'.join(output))
