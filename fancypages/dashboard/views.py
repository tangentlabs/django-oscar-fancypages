from django import http
from django.views import generic
from django.contrib import messages
from django.db.models import get_model, Q
from django.utils import simplejson as json
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _

from fancypages.dashboard import forms
from fancypages.views import PageDetailView


Page = get_model('fancypages', 'Page')
PageTemplate = get_model('fancypages', 'PageTemplate')
PageType = get_model('fancypages', 'PageType')
Widget = get_model('fancypages', 'Widget')
Container = get_model('fancypages', 'Container')


class PageTemplateListView(generic.ListView):
    model = PageTemplate
    context_object_name = 'page_template_list'
    template_name = "fancypages/dashboard/page_template_list.html"


class PageTemplateCreateView(generic.CreateView):
    model = PageTemplate
    form_class = forms.PageTemplateForm
    context_object_name = 'page_template'
    template_name = "fancypages/dashboard/page_template_update.html"

    def get_context_data(self, **kwargs):
        ctx = super(PageTemplateCreateView, self).get_context_data(**kwargs)
        ctx['page_title'] = _("Create new page template")
        return ctx

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-template-list')


class PageTemplateUpdateView(generic.UpdateView):
    model = PageTemplate
    form_class = forms.PageTemplateForm
    context_object_name = 'page_template'
    template_name = "fancypages/dashboard/page_template_update.html"

    def get_context_data(self, **kwargs):
        ctx = super(PageTemplateUpdateView, self).get_context_data(**kwargs)
        ctx['page_title'] = _("Update page template")
        return ctx

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-template-list')


class PageTemplateDeleteView(generic.DeleteView):
    model = PageTemplate
    context_object_name = 'page_template'
    template_name = "fancypages/dashboard/page_template_delete.html"

    def get_success_url(self):
        return reverse('fancypages-dashboard:page-template-list')


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


class PagePreviewView(PageDetailView):

    def get_context_data(self, **kwargs):
        ctx = super(PagePreviewView, self).get_context_data(**kwargs)
        ctx['edit_mode'] = True
        ctx['widget_create_form'] = forms.WidgetCreateSelectForm()
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
        return reverse(
            'fancypages-dashboard:page-customise',
            args=(self.object.id,)
        )


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


class WidgetSelectView(generic.ListView):
    model = Widget
    template_name = "fancypages/dashboard/widget_select.html"

    def get(self, request, *args, **kwargs):
        container_id = self.kwargs.get('container_id')
        self.container = Container.objects.get(id=container_id)
        return super(WidgetSelectView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        container_id = self.kwargs.get('container_id')
        self.container = Container.objects.get(id=container_id)
        return super(WidgetSelectView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WidgetSelectView, self).get_context_data(**kwargs)
        ctx['container'] = self.container
        ctx['add_widget_form'] = forms.WidgetCreateSelectForm()
        return ctx


class WidgetAddView(generic.CreateView):
    model = Widget
    template_name = "fancypages/dashboard/widget_create.html"

    def get_initial(self):
        return {
            'display_order': self.container.widgets.count(),
        }

    def get(self, request, *args, **kwargs):
        container_id = self.kwargs.get('container_id')
        self.container = Container.objects.get(id=container_id)
        return super(WidgetCreateView, self).get(request, *args, **kwargs)


class WidgetCreateView(generic.CreateView, FancypagesMixin):
    model = Widget
    template_name = "fancypages/dashboard/widget_create.html"

    def get_initial(self):
        return {
            'display_order': self.container.widgets.count(),
        }

    def get(self, request, *args, **kwargs):
        container_id = self.kwargs.get('container_id')
        self.container = Container.objects.get(id=container_id)
        return super(WidgetCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        container_id = self.kwargs.get('container_id')
        self.container = Container.objects.get(id=container_id)
        return super(WidgetCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(WidgetCreateView, self).get_context_data(**kwargs)
        ctx['container'] = self.container
        ctx['widget_code'] = self.kwargs.get('code')
        return ctx

    def get_form_class(self):
        model = self.get_widget_class()
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


class WidgetUpdateView(generic.UpdateView, FancypagesMixin):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_update.html"

    def get_object(self, queryset=None):
        return self.get_widget_object()

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
        return reverse('fancypages-dashboard:page-list')


class JSONResponseMixin(object):

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class WidgetMoveView(JSONResponseMixin, generic.edit.BaseDetailView,
                     FancypagesMixin):
    model = Widget

    def get_object(self, queryset=None):
        return self.get_widget_object()

    def get_context_data(self, **kwargs):
        moved_widget = self.get_object()

        if not moved_widget:
            return {
                'success': False,
                'reason': "widget does not exist"
            }

        new_pos = int(self.kwargs.get('index'))

        if new_pos == moved_widget.display_order:
            return {
                'success': True
            }

        if new_pos > moved_widget.display_order:
            widgets = moved_widget.container.widgets.filter(
                ~Q(id=moved_widget.id) &
                Q(display_order__lte=new_pos)
            )
            for idx, widget in enumerate(widgets):
                widget.display_order = idx
                widget.save()

        else:
            widgets = moved_widget.container.widgets.filter(
                ~Q(id=moved_widget.id) &
                Q(display_order__gte=new_pos)
            )
            for idx, widget in enumerate(widgets):
                widget.display_order = new_pos + idx + 1
                widget.save()

        moved_widget.display_order = new_pos
        moved_widget.save()

        return {
            'success': True,
        }


class ContainerAddWidgetView(JSONResponseMixin, generic.edit.BaseDetailView,
                             FancypagesMixin):
    model = Container

    def get_context_data(self, **kwargs):
        widget_code = self.kwargs.get('code', None)
        if widget_code is None:
            return {
                'success': False,
                'error': "could not find valid widget code"
            }

        model = self.get_widget_class()
        if model is None:
            return {
                'success': False,
                'error': "could not find widget with code %s" % widget_code
            }

        # create a new widget and add it to the given container
        widget = model.objects.create(
            container=self.object,
            display_order=self.object.widgets.count(),
        )
        return {
            'success': True,
            'update_url': reverse(
                'fancypages-dashboard:widget-update',
                args=(widget.id,)
            )
        }
