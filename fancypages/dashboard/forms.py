from django import forms
from django.db.models import get_model
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from fancypages.widgets import SelectWidgetRadioFieldRenderer

Page = get_model('fancypages', 'Page')
Category = get_model('catalogue', 'Category')
PageType = get_model('fancypages', 'PageType')


class PageForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        if 'page_type' in self.fields:
            self.fields['page_type'].queryset = PageType.objects.all()

    def save(self, commit=True):
        page_name = self.cleaned_data['name']
        self.instance.category.name = page_name
        self.instance.category.save()
        return super(PageForm, self).save(commit=True)

    class Meta:
        model = Page
        fields = ['name', 'keywords', 'page_type',
                  'status', 'date_visible_start',
                  'date_visible_end', 'is_active']


class PageCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        parent_id = kwargs.pop('parent_pk', None)
        super(PageCreateForm, self).__init__(*args, **kwargs)
        try:
            self.parent = Category.objects.get(id=parent_id)
        except Category.DoesNotExist:
            self.parent = None
        if 'page_type' in self.fields:
            self.fields['page_type'].queryset = PageType.objects.all()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Page.objects.get(category__slug=slugify(name))
        except Page.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                _("A page with this title already exists")
            )
        return name

    def save(self, commit=True):
        page_name = self.cleaned_data['name']
        if self.parent:
            category = self.parent.add_child(name=page_name)
        else:
            category = Category.add_root(name=page_name)
        instance = super(PageCreateForm, self).save(commit=False)
        # this is a bit of a hack but we cannot create a new
        # instance here because it has already been created using
        # a post_save signal on the category.
        instance.id = category.page.id
        instance.category = category
        instance.save()
        return instance

    class Meta:
        model = Page
        fields = ['name', 'keywords', 'page_type',
                  'status', 'date_visible_start',
                  'date_visible_end', 'is_active']


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
    template_name = "fancypages/partials/editor_form_fields.html"

    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput()
        }


class AssetWidgetForm(WidgetForm):
    template_name = 'fancypages/widgets/assetwidget_form.html'
    asset_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    asset_type = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(AssetWidgetForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.asset = instance.image_asset
        if instance and instance.image_asset:
            self.fields['asset_id'].initial = instance.image_asset.id
            self.fields['asset_type'].initial = instance.image_asset.asset_type

    def clean(self):
        asset_type = self.cleaned_data.get('asset_type')
        asset_id = self.cleaned_data.get('asset_id')
        if not asset_type and not asset_id:
            return self.cleaned_data

        model = get_model('assets', asset_type)
        if model is None:
            raise forms.ValidationError(
                "asset type %s is invalid" % asset_type
            )

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
        if asset_id:
            model = get_model('assets', self.cleaned_data['asset_type'])
            instance.image_asset = model.objects.get(id=asset_id)

        if commit:
            instance.save()
        return instance

    class Meta:
        abstract = True


class TextWidgetForm(WidgetForm):
    class Meta:
        exclude = ('container',)
        widgets = {
            'display_order': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class TitleTextWidgetForm(WidgetForm):
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


class TwoColumnLayoutWidgetForm(WidgetForm):
    left_width = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'data-min': 1,
            # the max value is restricted to '11' in JS but we need the actual
            # max value there so this is the way to pass it through
            'data-max': 12,
        }),
        label=_("Proportion of columns")
    )


class TabWidgetForm(WidgetForm):

    def __init__(self, *args, **kwargs):
        super(TabWidgetForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']
        if instance:
            for tab in instance.tabs.all():
                field_name = "tab_title_%d" % tab.id
                self.fields[field_name] = forms.CharField()
                self.fields[field_name].initial = tab.title
                self.fields[field_name].label = _("Tab title")

    def save(self):
        instance = super(TabWidgetForm, self).save()

        for tab in instance.tabs.all():
            field_name = "tab_title_%d" % tab.id
            tab.title = self.cleaned_data[field_name]
            tab.save()

        return instance
