from django.db.models import get_model
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from fancypages import test

Page = get_model('fancypages', 'Page')
Widget = get_model('fancypages', 'Widget')
PageType = get_model('fancypages', 'PageType')
TextWidget = get_model('fancypages', 'TextWidget')
PageTemplate = get_model('fancypages', 'PageTemplate')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAWidget(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAWidget, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fancypages_container page-container %}"
        )

        self.page = Page.add_root(title="A new page", slug='a-new-page')

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

    def test_can_be_added_to_a_container(self):
        container = self.page.get_container_from_name('page-container')
        num_widgets = container.widgets.count()
        response = self.post(
            reverse('fp-api:widget-list'),
            params={
                'container': container.id,
                'code': self.text_widget.code,
            },
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(container.widgets.count(), num_widgets + 1)

    def test_a_widget_without_template_is_ignored(self):
        container = self.page.get_container_from_name('page-container')
        Widget.objects.create(container=container)
        self.get(reverse('fancypages:page-detail', args=(self.page.slug,)))


class TestAMovableWidget(test.FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True

    def setUp(self):
        super(TestAMovableWidget, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fancypages_container main-container %}"
            "{% fancypages_container left-container %}"
        )

        self.page = Page.add_root(title="A new page", slug='a-new-page',
                                  template_name=self.template_name)
        self.left_container = self.page.get_container_from_name('left-container')
        self.main_container = self.page.get_container_from_name('main-container')

        self.left_widgets = []
        self.main_widgets = []

        for idx in range(0, 3):
            main_widget = TextWidget.objects.create(
                container=self.main_container,
                text="Main Column / Widget #%d" % idx,
            )
            self.main_widgets.append(main_widget)
            self.assertEquals(main_widget.display_order, idx)

            left_widget = TextWidget.objects.create(
                container=self.left_container,
                text="Left Column / Widget #%d" % idx,
            )
            self.left_widgets.append(left_widget)
            self.assertEquals(left_widget.display_order, idx)

    def test_can_be_moved_up_within_a_container(self):
        for idx, pos in [(0, 0), (1, 1), (2, 2)]:
            self.assertEquals(
                TextWidget.objects.get(id=self.left_widgets[idx].id).display_order,
                pos
            )

        self.get(
            reverse(
                'fp-dashboard:widget-move',
                kwargs={
                    'pk': self.main_widgets[1].id,
                    'container_pk': self.left_container.id,
                    'index': 1,
                }
            )
        )

        moved_widget = TextWidget.objects.get(id=self.main_widgets[1].id)
        self.assertEquals(
            moved_widget.container,
            self.page.get_container_from_name('left-container')
        )
        self.assertEquals(moved_widget.display_order, 1)

        for idx, pos in [(0, 0), (1, 2), (2, 3)]:
            self.assertEquals(
                TextWidget.objects.get(id=self.left_widgets[idx].id).display_order,
                pos
            )

        for idx, pos in [(0, 0), (2, 1)]:
            self.assertEquals(
                TextWidget.objects.get(id=self.main_widgets[idx].id).display_order,
                pos
            )
