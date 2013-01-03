from webtest import AppError

from django.db.models import get_model
from django.core.urlresolvers import reverse
from oscar_testsupport.factories import create_product

from fancypages.test import FancyPagesWebTest


Page = get_model('fancypages', 'Page')
Container = get_model('fancypages', 'Container')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAnAnonymousUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_anonymous = True

    def setUp(self):
        super(TestAnAnonymousUser, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fancypages_container main-container %}"
            "{% fancypages_container left-column %}"
        )
        self.page = Page.add_root(
            title="A new page",
            slug='a-new-page',
            template_name=self.template_name,
        )

        self.left_container = self.page.get_container_from_name('left-column')
        self.main_container = self.page.get_container_from_name('main-container')

        self.main_widget = TitleTextWidget.objects.create(
            container=self.main_container,
            title="This is the main title",
            text="The text of the main widget",
        )

        self.left_widget = TitleTextWidget.objects.create(
            container=self.left_container,
            title="This is the left title",
            text="The text of the left widget",
        )

    def test_cannot_view_a_draft_page(self):
        self.assertRaises(
            AppError,
            self.get,
            reverse('fancypages:page-detail', args=(self.page.slug,))
        )

    def test_can_view_a_published_page(self):
        self.page.status = Page.PUBLISHED
        self.page.save()

        page = self.get(reverse('fancypages:page-detail', args=(self.page.slug,)))
        self.assertContains(page, self.left_widget.title)
        self.assertContains(page, self.main_widget.title)


class TestAStaffUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True

    def setUp(self):
        super(TestAStaffUser, self).setUp()
        #self.prepare_template_file(
        #    "{% load fp_container_tags%}"
        #    "{% fancypages_container main-container %}"
        #    "{% fancypages_container left-column %}"
        #)
        self.page = Page.add_root(title="A new page", slug='a-new-page')
        self.page_container = self.page.get_container_from_name('page-container')

        self.main_widget = TitleTextWidget.objects.create(
            container=self.page_container,
            title="This is the main title",
            text="The text of the main widget",
        )

    def test_can_view_a_draft_page(self):
        url = reverse('fancypages:page-detail', args=(self.page.slug,))
        page = self.get(url)

        self.assertContains(page, self.main_widget.title)

        self.assertContains(
            page,
            ("You can only see this because you are logged in as "
             "a user with access rights to the dashboard")
        )

    def test_can_view_a_published_page(self):
        self.page.status = Page.PUBLISHED
        self.page.save()

        page = self.get(reverse('fancypages:page-detail', args=(self.page.slug,)))
        self.assertContains(page, self.main_widget.title)

        self.assertNotContains(
            page,
            ("You can only see this because you are logged in as "
             "a user with access rights to the dashboard")
        )

    def test_can_customise_a_product_page(self):
        product = create_product()
        self.assertEquals(len(Container.get_containers(product)), 0)

        # Loading this page creates the missing containers
        from fancypages.templatetags.fp_container_tags import get_customise_url
        self.get(get_customise_url({}, product))

        # We need to get the preview page separately because it is
        # rendered in an iframe and so the markup is not available in
        # the parent page
        from fancypages.templatetags.fp_container_tags import get_preview_url
        page = self.get(get_preview_url({}, product))

        self.assertEquals(len(Container.get_containers(product)), 4)
        self.assertContains(page, "Add content")
