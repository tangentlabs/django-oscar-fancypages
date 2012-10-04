from django.views import generic
from django.contrib import messages
from django.db.models import get_model
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_class

from fancypages.dashboard import forms


Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')
Widget = get_model('fancypages', 'Widget')
Container = get_model('fancypages', 'Container')


class PageTypeListView(generic.ListView):
    model = PageType
    context_object_name = 'page_type_list'
    template_name = "fancypages/dashboard/page_type_list.html"


class PageTypeCreateView(generic.CreateView):
    model = PageType
    form_class = forms.PageTypeForm
    context_object_name = 'page_type'
    template_name = "fancypages/dashboard/page_type_update.html"

    def get_context_data(self, **kwargs):
        ctx = super(PageTypeCreateView, self).get_context_data(**kwargs)
        ctx['page_title'] = _("Create new page type")
        return ctx

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-type-list')


class PageTypeUpdateView(generic.UpdateView):
    model = PageType
    form_class = forms.PageTypeForm
    context_object_name = 'page_type'
    template_name = "fancypages/dashboard/page_type_update.html"

    def get_context_data(self, **kwargs):
        ctx = super(PageTypeUpdateView, self).get_context_data(**kwargs)
        ctx['page_title'] = _("Update page type %s") % self.object.name
        return ctx

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-type-list')


class PageTypeDeleteView(generic.DeleteView):
    model = PageType
    context_object_name = 'page_type'
    template_name = "fancypages/dashboard/page_type_delete.html"

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-type-list')


class PageListView(generic.ListView):
    model = Page
    context_object_name = 'page_list'
    template_name = "fancypages/dashboard/page_list.html"

    def get_context_data(self, **kwargs):
        ctx = super(PageListView, self).get_context_data(**kwargs)
        ctx['page_type_form'] = forms.PageTypeSelectForm()
        return ctx


class PageCreateRedirectView(generic.RedirectView):

    def get_redirect_url(self, **kwargs):
        page_type_code = self.request.GET.get('page_type', None)

        if not page_type_code:
            messages.error(self.request, _("Please select a page type"))
            return reverse('fancypages-dashboard:page-list')

        try:
            page_type = PageType.objects.get(code=page_type_code)
        except PageType.DoesNotExist:
            messages.error(self.request, _("Please select a page type"))
            return reverse('fancypages-dashboard:page-list')

        return reverse('fancypages-dashboard:page-create',
                       kwargs={'page_type_code': page_type.code})


class PageCreateView(generic.CreateView):
    template_name = "fancypages/dashboard/page_update.html"
    form_class = forms.PageForm
    model = Page

    def get_context_data(self, **kwargs):
        ctx = super(PageCreateView, self).get_context_data(**kwargs)
        ctx['page_type'] = self.page_type
        return ctx

    def get_form(self, form_class):
        return form_class(self.page_type, **self.get_form_kwargs())

    def get_page_type(self):
        code = self.kwargs.get('page_type_code', None)
        try:
            page_type = PageType.objects.get(code=code)
        except PageType.DoesNotExist:
            page_type = None
        return page_type

    def get(self, request, **kwargs):
        self.page_type = self.get_page_type()
        return super(PageCreateView, self).get(request, **kwargs)

    def post(self, request, **kwargs):
        self.page_type = self.get_page_type()
        return super(PageCreateView, self).post(request, **kwargs)

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-list')


class PageUpdateView(generic.UpdateView):
    template_name = "fancypages/dashboard/page_update.html"
    context_object_name = 'page'
    form_class = forms.PageForm
    model = Page

    def get_context_data(self, **kwargs):
        ctx = super(PageUpdateView, self).get_context_data(**kwargs)
        return ctx

    def get_form(self, form_class):
        return form_class(
            self.object.page_type,
            **self.get_form_kwargs()
        )

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-list')


class PageCustomiseView(PageUpdateView):
    template_name = "fancypages/dashboard/page_customise.html"

    def get_context_data(self, **kwargs):
        ctx = super(PageCustomiseView, self).get_context_data(**kwargs)
        ctx['select_widget_form'] = forms.WidgetCreateSelectForm()
        return ctx

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-list')


class WidgetCreateView(generic.CreateView):
    model = Widget
    template_name = "fancypages/dashboard/widget_create.html"

    def get_initial(self):
        return {
            'display_order': self.container.widgets.count(),
        }

    def get(self, request, *args, **kwargs):
        container_name = self.kwargs.get('container_name')
        self.container = Container.objects.get(variable_name=container_name)
        return super(WidgetCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        container_name = self.kwargs.get('container_name')
        self.container = Container.objects.get(variable_name=container_name)
        return super(WidgetCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WidgetCreateView, self).get_context_data(**kwargs)
        ctx['container'] = self.container
        ctx['widget_code'] = self.kwargs.get('code')
        return ctx

    def get_form_class(self):
        for widget_class in Widget.itersubclasses():
            if widget_class._meta.abstract:
                continue

            if widget_class.code == self.kwargs.get('code'):
                model = widget_class
                break

        form_class = getattr(forms, "%sForm" % model.__name__, forms.WidgetForm)
        form_class = modelform_factory(model, form=form_class)
        return form_class

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.container = self.container
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('fancypages-dashboard:widget-update',
                       args=(self.object.id,))


class WidgetUpdateView(generic.UpdateView):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_update.html"

    def get_object(self, queryset=None):
        try:
            return self.model.objects.select_subclasses().get(
                id=self.kwargs.get('pk')
            )
        except self.model.DoesNotExist:
            return self.model.objects.none()

    def get_form_class(self):
        model = self.object.__class__
        form_class = getattr(
            forms,
            "%sForm" % model.__name__,
            forms.WidgetForm
        )
        return modelform_factory(model, form=form_class)

    def get_success_url(self):
        return reverse('fancypages-dashboard:widget-update',
                       args=(self.object.id,))
