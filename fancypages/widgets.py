from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape

from django.forms.widgets import RadioInput, RadioFieldRenderer


class SelectWidgetRadioInput(RadioInput):

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        return mark_safe(u'<label id="%s" %s>%s %s</label>' % (
            self.choice_value,
            label_for,
            self.tag(),
            choice_label
        ))


class SelectWidgetRadioFieldRenderer(RadioFieldRenderer):

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield SelectWidgetRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return SelectWidgetRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)
