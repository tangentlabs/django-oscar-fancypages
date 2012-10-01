from django import forms
from django.db.models import get_model


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
