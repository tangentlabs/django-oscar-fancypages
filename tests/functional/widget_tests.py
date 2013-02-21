from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages import test

Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
Page = get_model('fancypages', 'Page')
TextWidget = get_model('fancypages', 'TextWidget')
PageTemplate = get_model('fancypages', 'PageTemplate')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAWidget(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAWidget, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container page-container %}"
        )

        self.page = Page.add_root(name="A new page", slug='a-new-page')

        self.text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text",
        )

        self.other_text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="some text",
        )

        self.third_text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('page-container'),
            text="second text",
        )
        self.assertEquals(self.text_widget.display_order, 0)
        self.assertEquals(self.other_text_widget.display_order, 1)
        self.assertEquals(self.third_text_widget.display_order, 2)

    def test_can_be_deleted(self):
        page = self.get(reverse(
            'fp-dashboard:widget-delete',
            args=(self.third_text_widget.id,)
        ))
        # we need to fake a body as the template does not
        # contain that
        page.body = "<body>%s</body>" % page.body
        page = page.form.submit()

        self.assertEquals(TextWidget.objects.count(), 2)
        self.assertRaises(
            TextWidget.DoesNotExist,
            TextWidget.objects.get,
            id=self.third_text_widget.id
        )

    def test_can_be_deleted_and_remaining_widgets_are_reordered(self):
        page = self.get(reverse(
            'fp-dashboard:widget-delete',
            args=(self.other_text_widget.id,)
        ))
        # we need to fake a body as the template does not
        # contain that
        page.body = "<body>%s</body>" % page.body
        page = page.form.submit()

        self.assertEquals(TextWidget.objects.count(), 2)
        self.assertRaises(
            TextWidget.DoesNotExist,
            TextWidget.objects.get,
            id=self.other_text_widget.id
        )

        widget = TextWidget.objects.get(id=self.text_widget.id)
        self.assertEquals(widget.display_order, 0)

        widget = TextWidget.objects.get(id=self.third_text_widget.id)
        self.assertEquals(widget.display_order, 1)

    def test_a_widget_without_template_is_ignored(self):
        container = self.page.get_container_from_name('page-container')
        Widget.objects.create(container=container)
        self.get(reverse('fancypages:page-detail', args=(self.page.category.slug,)))
