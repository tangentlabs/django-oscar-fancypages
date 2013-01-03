from django import http
from django.views import generic
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from fancypages.dashboard import forms
from fancypages.views import PageDetailView
from fancypages.mixins import JSONResponseMixin
from fancypages.utils import get_container_names_from_template


Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
Container = get_model('fancypages', 'Container')
TabWidget = get_model('fancypages', 'TabWidget')
OrderedContainer = get_model('fancypages', 'OrderedContainer')


class PageListView(generic.ListView):
    model = Page
    context_object_name = 'page_list'
    template_name = "fancypages/dashboard/page_list.html"

    def get_queryset(self, queryset=None):
        return self.model.objects.filter(depth=1)


class PageCreateView(generic.CreateView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageForm
    model = Page

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class PageUpdateView(generic.UpdateView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageForm
    context_object_name = 'page'
    model = Page

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class PageDeleteView(generic.DeleteView):
    model = Page
    template_name = "fancypages/dashboard/page_delete.html"

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class PageCustomiseView(PageUpdateView):
    template_name = "fancypages/dashboard/page_customise.html"
    form_class = forms.PageForm

    def get_context_data(self, **kwargs):
        ctx = super(PageCustomiseView, self).get_context_data(**kwargs)
        ctx['select_widget_form'] = forms.WidgetCreateSelectForm()
        return ctx

    def get_success_url(self):
        return reverse(
            'fp-dashboard:page-customise',
            args=(self.object.id,)
        )


class PagePreviewView(PageDetailView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageForm
    edit_mode = True

    def get_context_data(self, **kwargs):
        ctx = super(PagePreviewView, self).get_context_data(**kwargs)
        ctx['widget_create_form'] = forms.WidgetCreateSelectForm()
        return ctx


class PageSelectView(generic.ListView):
    model = Page
    template_name = "fancypages/dashboard/page_select.html"

    def get_queryset(self, queryset=None):
        return self.model.objects.filter(depth=1)


class FancypagesMixin(object):

    def get_widget_class(self):
        model = None
        for widget_class in Widget.itersubclasses():
            if widget_class._meta.abstract:
                continue

            if widget_class.code == self.kwargs.get('code'):
                model = widget_class
                break
        return model

    def get_widget_object(self):
        try:
            return self.model.objects.select_subclasses().get(
                id=self.kwargs.get('pk')
            )
        except self.model.DoesNotExist:
            raise http.Http404


class WidgetUpdateView(generic.UpdateView, FancypagesMixin):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_update.html"

    def get_object(self, queryset=None):
        return self.get_widget_object()

    def get_form_kwargs(self):
        kwargs = super(WidgetUpdateView, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_form_class(self):
        model = self.object.__class__
        form_class = getattr(
            forms,
            "%sForm" % model.__name__,
            forms.WidgetForm
        )
        return modelform_factory(model, form=form_class)

    def get_success_url(self):
        return reverse('fp-dashboard:widget-update',
                       args=(self.object.id,))


class WidgetDeleteView(generic.DeleteView, FancypagesMixin):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_delete.html"

    def get_object(self, queryset=None):
        return self.get_widget_object()

    def delete(self, request, *args, **kwargs):
        response = super(WidgetDeleteView, self).delete(request, *args, **kwargs)
        for idx, widget in enumerate(self.object.container.widgets.all().select_subclasses()):
            widget.display_order = idx
            widget.save()
        return response

    def get_success_url(self):
        return reverse('fp-dashboard:page-list')


class ContentTypeMixin(object):

    def get_model(self):
        if not self.model:
            content_type = get_object_or_404(
                ContentType,
                id=self.kwargs.get('content_type_pk', None))
            self.model = content_type.model_class()
        return self.model

    def get_object(self, queryset=None):
        model = self.get_model()
        instance = get_object_or_404(model, id=self.kwargs.get('pk', None))

        cnames = get_container_names_from_template(
            self.get_content_page_template_name(model))
        for cname in cnames:
            Container.get_container_by_name(instance, cname)

        return instance

    def get_content_page_template_name(self, model):
        model_name = self.get_model().__name__.lower()
        return "fancypages/pages/%s_page.html" % model_name


class ContentCustomiseView(ContentTypeMixin, generic.DetailView):
    template_name = "fancypages/dashboard/content_customise.html"


class ContentPreviewView(ContentTypeMixin, generic.DetailView):

    def get_template_names(self):
        return [
            self.get_content_page_template_name(self.get_model())
        ]

    def get_context_data(self, **kwargs):
        ctx = super(ContentPreviewView, self).get_context_data(**kwargs)
        ctx['edit_mode'] = True
        ctx['widget_create_form'] = forms.WidgetCreateSelectForm()
        return ctx
