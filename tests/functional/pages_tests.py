from webtest import AppError

from django.db.models import get_model
from django.core.urlresolvers import reverse

from oscar.test.helpers import create_product

from fancypages.test import FancyPagesWebTest


Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')
PageTemplate = get_model('fancypages', 'PageTemplate')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAnAnonymousUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_anonymous = True

    def setUp(self):
        super(TestAnAnonymousUser, self).setUp()
        template = PageTemplate.objects.get(title="Article Template")
        self.page_type = PageType.objects.create(name='Article', code='article',
                                                 template=template)

        self.page = Page.add_root(
            title="A new page",
            slug='a-new-page',
            page_type=self.page_type,
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
        template = PageTemplate.objects.get(title="Article Template")
        self.page_type = PageType.objects.create(name='Article', code='article',
                                                 template=template)

        self.page = Page.add_root(
            title="A new page",
            slug='a-new-page',
            page_type=self.page_type,
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

    def test_can_view_a_draft_page(self):
        page = self.get(reverse('fancypages:page-detail', args=(self.page.slug,)))
        self.assertContains(page, self.left_widget.title)
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
        self.assertContains(page, self.left_widget.title)
        self.assertContains(page, self.main_widget.title)

        self.assertNotContains(
            page,
            ("You can only see this because you are logged in as "
             "a user with access rights to the dashboard")
        )

    def test_can_customise_a_product_page(self):
        product = create_product()
        self.assertEquals(product.containers.count(), 0)

        # Loading this page creates the missing containers
        self.get(reverse(
            'fp-dashboard:product-page-customise',
            args=(product.id,)
        ))

        # We need to get the preview page separately because it is
        # rendered in an iframe and so the markup is not available in
        # the parent page
        page = self.get(reverse(
            'fp-dashboard:product-page-preview',
            args=(product.id,)
        ))

        self.assertEquals(product.containers.count(), 4)
        self.assertContains(page, "Add content")
