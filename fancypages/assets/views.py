import json

from django.conf import settings
from django.views import generic
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages.assets import forms

ImageAsset = get_model('assets', 'ImageAsset')


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


class ImageListView(generic.ListView):
    model = ImageAsset
    template_name = 'fancypages/assets/image_list.html'
    context_object_name = 'image_list'


class ImageCreateView(generic.CreateView):
    model = ImageAsset
    template_name = 'fancypages/assets/image_update.html'
    form_class = forms.ImageAssetCreateForm
    thumbnail_template_name = 'fancypages/assets/partials/image_thumbnail.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.name = self.object.image.name
        self.object.creator = self.request.user
        self.object.save()

        f = self.request.FILES.get('image')

        template = loader.get_template(self.thumbnail_template_name)
        thumbnail_markup = template.render(RequestContext(self.request, {
            'image_asset': self.object,
        }))

        data = [{
            'name': f.name,
            'url': self.object.get_absolute_url(),
            'thumbnail_url': '',
            'image_markup': thumbnail_markup,
            'delete_url': '', #reverse('upload-delete', args=[self.object.id]),
            'delete_type': 'DELETE',
        }]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = json.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
