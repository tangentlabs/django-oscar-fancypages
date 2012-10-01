from django.views import generic
from django.contrib import messages
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from fancypages.dashboard.forms import PageTypeSelectForm


Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')


class PageListView(generic.ListView):
    template_name = "fancypages/dashboard/page_list.html"
    model = Page

    def get_context_data(self, **kwargs):
        ctx = super(PageListView, self).get_context_data(**kwargs)
        ctx['page_type_form'] = PageTypeSelectForm()
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
    model = Page

    def get_context_data(self, **kwargs):
        ctx = super(PageCreateView, self).get_context_data(**kwargs)
        ctx['page_type'] = self.page_type
        return ctx

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
