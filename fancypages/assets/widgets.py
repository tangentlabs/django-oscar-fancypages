import os

from django.conf import settings
from django.template import Context
from django.db.models import get_model
from django.forms.widgets import TextInput
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string
from django.forms.util import flatatt
from django.utils.safestring import mark_safe


ImageAsset = get_model('assets', 'ImageAsset')


class ImageAssetInput(TextInput):
    template_name = 'fancypages/assets/partials/image_asset_input.html'

    def render(self, name, value, attrs=None):
        try:
            image_asset = ImageAsset.objects.get(id=value)
        except ImageAsset.DoesNotExist:
            image_asset = None
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))

        ctx = {
            'input_attrs': flatatt(final_attrs),
            'image_asset': image_asset,
            'missing_image_url': os.path.join(
                settings.MEDIA_URL,
                getattr(settings, "OSCAR_MISSING_IMAGE_URL", '')
            )
        }
        return render_to_string(self.template_name, Context(ctx))
