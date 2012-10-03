import os

from django import forms
from django.conf import settings
from django.db.models import get_model


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
