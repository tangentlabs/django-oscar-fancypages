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


class AssetWidgetForm(forms.ModelForm):
    asset_id = forms.IntegerField(widget=forms.HiddenInput())
    asset_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(AssetWidgetForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.asset = instance.image_asset
        if instance and instance.image_asset:
            self.fields['asset_id'].initial = instance.image_asset.id
            self.fields['asset_type'].initial = instance.image_asset.asset_type

    def clean(self):
        asset_type = self.cleaned_data.get('asset_type', '')
        model = get_model('assets', asset_type)
        if model is None:
            raise forms.ValidationError("asset type %s is invalid" % asset_type)

        asset_id = self.cleaned_data.get('asset_id', None)
        try:
            self.asset = model.objects.get(id=asset_id)
        except model.DoesNotExist:
            raise forms.ValidationError(
                "asset with ID %s does not exist" % asset_id
            )
        return self.cleaned_data

    def save(self, commit=True):
        instance = super(AssetWidgetForm, self).save(commit=False)

        asset_id = self.cleaned_data['asset_id']
        model = get_model('assets', self.cleaned_data['asset_type'])

        instance.image_asset = model.objects.get(id=asset_id)

        if commit:
            instance.save()
        return instance

    class Meta:
        abstract = True


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


class ImageWidgetForm(AssetWidgetForm):
    asset_id = forms.IntegerField(widget=forms.HiddenInput())
    asset_type = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        exclude = ('container', 'image_asset')
        widgets = {
            'display_order': forms.HiddenInput(),
        }


class ImageAndTextWidgetForm(AssetWidgetForm):
    asset_id = forms.IntegerField(widget=forms.HiddenInput())
    asset_type = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        exclude = ('container', 'image_asset')
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TabbedBlockWidgetForm(WidgetForm):

    def __init__(self, *args, **kwargs):
        super(TabbedBlockWidgetForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        if instance:
            for tab in instance.tabs.all():
                field_name = "tab_title_%d" % tab.id
                self.fields[field_name] = forms.CharField()
                self.fields[field_name].initial = tab.title
                self.fields[field_name].label = _("Tab title")

    def save(self):
        instance = super(TabbedBlockWidgetForm, self).save()

        for tab in instance.tabs.all():
            field_name = "tab_title_%d" % tab.id
            tab.title = self.cleaned_data[field_name]
            tab.save()

        return instance
