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


class WidgetCreateView(generic.CreateView):
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


class WidgetDeleteView(generic.DeleteView):
    model = Widget
    context_object_name = 'widget'
    template_name = "fancypages/dashboard/widget_delete.html"

    def get_object(self, queryset=None):
        try:
            return self.model.objects.select_subclasses().get(
                id=self.kwargs.get('pk')
            )
        except self.model.DoesNotExist:
            return self.model.objects.none()

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
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class WidgetMoveView(JSONResponseMixin, generic.edit.BaseDetailView):
    model = Widget

    def get_object(self, queryset=None):
        try:
            return self.model.objects.select_subclasses().get(
                id=self.kwargs.get('pk')
            )
        except self.model.DoesNotExist:
            return self.model.objects.none()

    def get_context_data(self, **kwargs):
        moved_widget = self.get_object()

        if not moved_widget:
            return {
                'success': False,
                'reason': "widget does not exist"
            }

        new_pos = int(self.kwargs.get('index'))
        print 'new position', new_pos

        if new_pos == moved_widget.display_order:
            return {
                'success': True
            }

        if new_pos > moved_widget.display_order:
            print 'larger new pos'
            widgets = moved_widget.container.widgets.filter(
                ~Q(id=moved_widget.id) &
                Q(display_order__lte=new_pos)
            )
            for idx, widget in enumerate(widgets):
                print widget.id, widget.display_order, idx
                widget.display_order = idx
                widget.save()

        else:
            print 'smaller arger new pos'
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
