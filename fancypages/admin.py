from django import forms
from django.contrib import admin

from fancypages import models


class TextWidgetAdminForm(forms.ModelForm):
    class Meta:
        model = models.TextWidget
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class TextWidgetAdmin(admin.ModelAdmin):
    form = TextWidgetAdminForm


class TitleTextWidgetAdminForm(forms.ModelForm):
    class Meta:
        model = models.TitleTextWidget
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class TitleTextWidgetAdmin(admin.ModelAdmin):
    form = TitleTextWidgetAdminForm


admin.site.register(models.Page)
admin.site.register(models.PageType)
admin.site.register(models.PageTemplate)
admin.site.register(models.Container)
admin.site.register(models.Widget)
admin.site.register(models.TextWidget, TextWidgetAdmin)
admin.site.register(models.TitleTextWidget, TitleTextWidgetAdmin)
admin.site.register(models.ImageWidget)
admin.site.register(models.TabbedBlockWidget)
admin.site.register(models.TabContainer)
