from django import forms
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.template import loader, TemplateDoesNotExist

from treebeard.forms import MoveNodeForm

from fancypages.widgets import SelectWidgetRadioFieldRenderer

Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')
PageTemplate = get_model('fancypages', 'PageTemplate')


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


class PageTemplateForm(forms.ModelForm):

    def clean_template_name(self):
        template_name = self.cleaned_data['template_name']
        try:
            loader.get_template(template_name)
        except TemplateDoesNotExist:
            raise forms.ValidationError(
                "template %s does not exist please enter the path of "
                "an existing template" % template_name
            )
        return template_name


    class Meta:
        model = PageTemplate


class PageTypeForm(forms.ModelForm):
    class Meta:
        model = PageType
        widgets = {
            'description': forms.Textarea(attrs={'row': 10, 'cols': 80}),
        }


class PageForm(MoveNodeForm):

    def __init__(self, page_type, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['page_type'].initial = page_type

    def save(self, commit=True):
        instance = super(PageForm, self).save(commit=False)

        if commit:
            instance.save()

        return instance

    class Meta:
        model = Page
        exclude = ('depth', 'numchild', 'path', 'slug',
                   'relative_url')
        widgets = {
            'page_type': forms.HiddenInput()
        }


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
