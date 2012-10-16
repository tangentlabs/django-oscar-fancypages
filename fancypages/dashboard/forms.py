import os

from django import forms
from django.conf import settings
from django.db.models import get_model
from django.forms.widgets import SubWidget
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.forms.util import flatatt, to_current_timezone
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext, ugettext_lazy
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from django.utils import datetime_safe, formats

Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')


class RadioInput(SubWidget):
    """
    An object used by RadioFieldRenderer that represents a single
    <input type='radio'>.
    """

    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = force_unicode(choice[0])
        self.choice_label = force_unicode(choice[1])
        self.index = index

    def __unicode__(self):
        return self.render()

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        if self.choice_value:
            return mark_safe(u'<label id="%s" %s>%s %s</label>' % (self.choice_value, label_for, self.tag(), choice_label))
        else:
            return mark_safe(u'<label %s>%s %s</label>' % (label_for, self.tag(), choice_label))

    def is_checked(self):
        return self.value == self.choice_value

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class RadioWidgetSelectRenderer(StrAndUnicode):
    """
    An object used by RadioSelect to enable customization of radio widgets.
    """

    def __init__(self, name, value, attrs, choices):
        self.name, self.value, self.attrs = name, value, attrs
        self.choices = choices

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return RadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def __unicode__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                % force_unicode(w) for w in self]))


class PageTypeSelectForm(forms.Form):
    page_type = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(PageTypeSelectForm, self).__init__(*args, **kwargs)

        page_type_choices = []
        for page_type in PageType.objects.all():
            page_type_choices.append(
                (page_type.code, page_type.name)
            )

        self.fields['page_type'].choices = page_type_choices


class PageTypeForm(forms.ModelForm):
    template_name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(PageTypeForm, self).__init__(*args, **kwargs)

        # TODO: this needs to be replaced with a template loader 
        # and specific fancy pages setting to load templates and
        # prevent filesystem IO on creation of every instance of
        # this form.
        template_dirs = getattr(settings, 'FANCYPAGES_TEMPLATE_DIRS', [])
        template_files = []
        for tdir in template_dirs:
            # we just look at files in the current directory and ignore
            # subdirectory as this is a temporary POC solution
            for tmpl_file in os.listdir(tdir):
                if tmpl_file.endswith('.html'):
                    template_files.append((tmpl_file, tmpl_file))

        self.fields['template_name'].choices = template_files

    class Meta:
        model = PageType


class PageForm(forms.ModelForm):

    def __init__(self, page_type, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.page_type = page_type

    def save(self, commit=True):
        instance = super(PageForm, self).save(commit=False)
        instance.page_type = self.page_type

        if commit:
            instance.save()

        return instance

    class Meta:
        model = Page
        exclude = ('code', 'page_type', 'relative_url')


class WidgetCreateSelectForm(forms.Form):
    widget_code = forms.ChoiceField(label=_("Add a new widget:"), widget=forms.RadioSelect(renderer=RadioWidgetSelectRenderer))

    def __init__(self, *args, **kwargs):
        super(WidgetCreateSelectForm, self).__init__(*args, **kwargs)
        widget_model = get_model('fancypages', 'Widget')
        self.fields['widget_code'].choices = widget_model.get_available_widgets()


class WidgetUpdateSelectForm(forms.Form):
    widget_code = forms.ChoiceField(label=_("Edit widget:"))

    def __init__(self, container, *args, **kwargs):
        super(WidgetUpdateSelectForm, self).__init__(*args, **kwargs)

        widget_choices = []
        for widget in container.widgets.select_subclasses():
            widget_choices.append((widget.id, unicode(widget)))

        self.fields['widget_code'].choices = widget_choices


class WidgetForm(forms.ModelForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput()
        }


class TextWidgetForm(forms.ModelForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TitleTextWidgetForm(forms.ModelForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
