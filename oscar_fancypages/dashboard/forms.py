from copy import copy

from django import forms
from django.conf import settings
from django.db.models import get_model
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

try:
    from oscar.apps.dashboard.catalogue.forms import CategoryForm as BaseCategoryForm
except ImportError:
    from oscar.apps.dashboard.catalogue.forms import BaseCategoryForm


FancyPage = get_model('fancypages', 'FancyPage')
Category = get_model('catalogue', 'Category')
PageType = get_model('fancypages', 'PageType')
VisibilityType = get_model('fancypages', 'VisibilityType')


DATE_FORMAT = getattr(settings, 'FANCYPAGES_DATE_FORMAT', '%Y-%m-%d')


FANCYPAGE_FORM_FIELDS = [
    'name',
    'description',
    'image',
    'keywords',
    'page_type',
    'status',
    'date_visible_start',
    'date_visible_end',
    'visibility_types',
]


class FancyPageFormMixin(object):

    def _inject_node_position(self):
        """ delete auxilary fields not belonging to node model """
        self.cleaned_data['_ref_node_id'] = 0
        self.cleaned_data['_position'] = 'first-child'

    def set_field_choices(self):
        if 'page_type' in self.fields:
            self.fields['page_type'].queryset = PageType.objects.all()
        if 'visibility_types' in self.fields:
            self.fields['visibility_types'].queryset = VisibilityType.objects.all()


class FancyPageForm(FancyPageFormMixin, BaseCategoryForm):
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=True)
    date_visible_start = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    date_visible_end = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    visibility_types = forms.ModelMultipleChoiceField(
        VisibilityType.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(FancyPageForm, self).__init__(*args, **kwargs)
        self.set_field_choices()
        self.fields.keyOrder = FANCYPAGE_FORM_FIELDS

    class Meta:
        model = FancyPage
        fields = FANCYPAGE_FORM_FIELDS


class FancyPageCreateForm(FancyPageFormMixin, BaseCategoryForm):
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    page_type = forms.ModelChoiceField(PageType.objects.none(), required=True)
    date_visible_start = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    date_visible_end = forms.DateTimeField(
        widget=forms.DateInput(format=DATE_FORMAT),
        input_formats=[DATE_FORMAT],
        required=False
    )
    visibility_types = forms.ModelMultipleChoiceField(
        VisibilityType.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        parent_id = kwargs.pop('parent_pk', None)
        super(FancyPageCreateForm, self).__init__(*args, **kwargs)

        try:
            self.parent = FancyPage.objects.get(id=parent_id)
        except FancyPage.DoesNotExist:
            self.parent = None

        self.set_field_choices()
        self.fields.keyOrder = FANCYPAGE_FORM_FIELDS

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            FancyPage.objects.get(slug=slugify(name))
        except FancyPage.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(
                _("A page with this title already exists")
            )
        return name

    def save(self, *args, **kwargs):
        page_kwargs = copy(self.cleaned_data)
        page_kwargs.pop('visibility_types')
        return FancyPage.add_root(**page_kwargs)

    class Meta:
        model = FancyPage
        fields = FANCYPAGE_FORM_FIELDS


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
