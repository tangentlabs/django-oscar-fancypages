import os
from PIL import Image
import tempfile

from django.test import TestCase
from django.core.files import File
from django.template import loader, Context
from django.contrib.auth.models import User
from django.forms.models import modelform_factory

from fancypages.models.base import Container
from fancypages.assets.models import ImageAsset
from fancypages.models.widgets import ImageWidget
from fancypages.dashboard.forms import WidgetForm


class TestAnImageAssetForm(TestCase):

    def setUp(self):
        __, self.filename = tempfile.mkstemp(prefix="assetformtest", suffix='.jpg')
        im = Image.new("RGB", (200, 200), color=(255, 0, 0))
        im.save(self.filename, "JPEG")
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@somwhere.com",
            password='pwd'
        )

    def tearDown(self):
        os.remove(self.filename)

    def test_contains_asset_input_fields(self):
        container = Container.objects.create(variable_name='test-container')
        image_asset = ImageAsset.objects.create(
            image=File(open(self.filename)),
            creator=self.user,
        )
        widget = ImageWidget.objects.create(
            container=container,
            image_asset=image_asset,
        )

        form_class = modelform_factory(ImageWidget, form=WidgetForm)
        tmpl = loader.get_template("fancypages/dashboard/widget_update.html")
        ctx = Context(
            {
                'widget': widget,
                'form': form_class(),
            }
        )
        form = tmpl.render(ctx)

        self.assertIn('name="image_asset_id"', form)
        self.assertIn('name="image_asset_type"', form)
