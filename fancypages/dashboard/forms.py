import os

from django import forms
from django.conf import settings
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _

from fancypages.widgets import SelectWidgetRadioFieldRenderer

Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')


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
        from django.utils.importlib import import_module
        base_dir = os.path.dirname(import_module('fancypages').__file__)
        template_dirs = [os.path.join(base_dir, 'templates/fancypages/pages')]
        template_dirs += getattr(settings, 'FANCYPAGES_TEMPLATE_DIRS', [])

        template_files = set()
        for tdir in template_dirs:
            # we just look at files in the current directory and ignore
            # subdirectory as this is a temporary POC solution
            for tmpl_file in os.listdir(tdir):
                if tmpl_file.endswith('.html'):
                    template_files.add((tmpl_file, tmpl_file))

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
    widget_code = forms.ChoiceField(
        label=_("Add a new widget:"),
        widget=forms.RadioSelect(renderer=SelectWidgetRadioFieldRenderer)
    )

    def __init__(self, *args, **kwargs):
        super(WidgetCreateSelectForm, self).__init__(*args, **kwargs)
        choices = get_model('fancypages', 'Widget').get_available_widgets()
        self.fields['widget_code'].choices = choices

        if len(choices):
            self.fields['widget_code'].initial = choices[0][0]


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
