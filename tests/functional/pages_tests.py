from webtest import AppError

from django.conf import settings
from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages.test import FancyPagesWebTest
from fancypages.views import PageDetailView


Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')
Container = get_model('fancypages', 'Container')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAnAnonymousUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_anonymous = True

    def setUp(self):
        super(TestAnAnonymousUser, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container main-container %}"
            "{% fp_object_container left-column %}"
        )
        page_type = PageType.objects.create(
            name='template',
            template_name=self.template_name
        )
        self.page = Page.add_root(
            name="A new page",
            slug='a-new-page',
            page_type=page_type,
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
            reverse('fancypages:page-detail', args=(self.page.category.slug,))
        )

    def test_can_view_a_published_page(self):
        self.page.status = Page.PUBLISHED
        self.page.save()

        page = self.get(reverse('fancypages:page-detail', args=(self.page.category.slug,)))
        self.assertContains(page, self.left_widget.title)
        self.assertContains(page, self.main_widget.title)


class TestAStaffUser(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True

    def setUp(self):
        super(TestAStaffUser, self).setUp()
        self.page = Page.add_root(name="A new page", slug='a-new-page')
        self.page_container = self.page.get_container_from_name('page-container')

        self.main_widget = TitleTextWidget.objects.create(
            container=self.page_container,
            title="This is the main title",
            text="The text of the main widget",
        )

    def test_can_view_a_draft_page(self):
        url = reverse('fancypages:page-detail', args=(self.page.category.slug,))
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

        page = self.get(reverse('fancypages:page-detail',
                                args=(self.page.category.slug,)))
        self.assertContains(page, self.main_widget.title)

        self.assertNotContains(
            page,
            ("You can only see this because you are logged in as "
             "a user with access rights to the dashboard")
        )


class TestAFancyPage(FancyPagesWebTest):
    fixtures = ['page_templates.json']
    is_staff = True

    def setUp(self):
        super(TestAFancyPage, self).setUp()
        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fp_object_container main-container %}"
            "{% fp_object_container left-column %}"
        )
        self.new_page_type = PageType.objects.create(
            name='template',
            template_name=self.template_name
        )

        self.page = Page.add_root(name="A new page", slug='a-new-page')
        self.page_container = self.page.get_container_from_name('page-container')

        self.child_page = self.page.add_root(
            name="Child page",
            slug="child-page",
            page_type=self.new_page_type,
        )
        self.child_container = self.child_page.get_container_from_name('page-container')

    def test_correct_category_is_placed_in_the_context(self):
        page = self.get(reverse('fancypages:page-detail',
                                kwargs={'category_slug': self.page.slug}))

        self.assertIn('category', page.context)
        self.assertEquals(page.context['category'], self.page.category)
        self.assertIn('fancypage', page.context)
        self.assertEquals(page.context['fancypage'], self.page)

    def test_correct_category_is_placed_in_the_context_for_child_page(self):
        page = self.get(reverse('fancypages:page-detail',
                                kwargs={'category_slug': self.child_page.slug}))

        self.assertIn('category', page.context)
        self.assertEquals(page.context['category'], self.child_page.category)
        self.assertIn('fancypage', page.context)
        self.assertEquals(page.context['fancypage'], self.child_page)

    def test_uses_default_template_without_page_type(self):
        view = PageDetailView()
        view.object = self.page
        templates = view.get_template_names()
        self.assertEquals([settings.FP_DEFAULT_TEMPLATE], templates)

    def test_uses_correct_page_type_template(self):
        view = PageDetailView()
        view.object = self.child_page
        templates = view.get_template_names()
        self.assertEquals([self.new_page_type.template_name], templates)
