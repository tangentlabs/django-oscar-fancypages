from webtest import AppError

from django import http
from django.conf import settings
from django.db.models import get_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

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


class TestAPublishedPage(FancyPagesWebTest):
    is_anonymous = True
    fixtures = ['page_templates.json']

    def setUp(self):
        super(TestAPublishedPage, self).setUp()
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

        self.glitter_main = Site.objects.get(id=1)
        self.glitter_main.domain = 'glitterbox.com'
        self.glitter_main.name = "Main Glitterbox"
        self.glitter_main.save()

        subdomains = [
            'm.glitterbox.com',
            'subdomain.glitterbox.com',
            'm.subdomain.glitterbox.com'
        ]

        for subdomain in subdomains:
            Site.objects.create(
                domain=subdomain,
                name="Subdomain '%s'" % subdomain
            )
        self.glitter_sub = Site.objects.get(domain="subdomain.glitterbox.com")

        self.page.status = Page.PUBLISHED
        self.page.save()

        self.abs_url = reverse('fancypages:page-detail', args=[self.page.slug])
        self.main_url = "http://%s%s" % (
            self.glitter_main.domain,
            self.abs_url
        )
        self.sub_url = "http://%s%s" % (
            self.glitter_sub.domain,
            self.abs_url
        )
        self.old_site_id = settings.SITE_ID

    def tearDown(self):
        settings.SITE_ID = settings.SITE_ID

    def set_current_site(self, site):
        settings.SITE_ID = site.id

    def test_can_be_viewed_on_both_domains(self):
        self.set_current_site(self.glitter_main)
        page = self.get(self.main_url)
        self.assertContains(page, self.main_widget.title)

        self.set_current_site(self.glitter_sub)
        page = self.get(self.sub_url)
        self.assertContains(page, self.main_widget.title)

    def test_can_only_be_viewed_on_main(self):
        self.page.display_on_sites.add(self.glitter_main)

        self.set_current_site(self.glitter_main)
        page = self.get(self.main_url)
        self.assertContains(page, self.main_widget.title)

        self.set_current_site(self.glitter_sub)
        self.assertRaises(AppError, self.get, self.sub_url)

    def test_can_only_be_viewed_on_subdomain(self):
        self.page.display_on_sites.add(self.glitter_sub)

        self.set_current_site(self.glitter_sub)
        page = self.get(self.sub_url)
        self.assertContains(page, self.main_widget.title)

        self.set_current_site(self.glitter_main)
        self.assertRaises(AppError, self.get, self.main_url)

    def test_can_not_be_seen_on_mobile_channel(self):
        self.page.visible_on_mobile = False
        self.page.save()

        self.set_current_site(self.glitter_sub)
        page = self.get(self.sub_url)
        self.assertContains(page, self.main_widget.title)

        mobile_sub_url = 'm.%s' % self.glitter_sub.domain
        mobile_site = Site.objects.get(domain=mobile_sub_url)
        self.set_current_site(mobile_site)

        self.sub_url = "http://%s%s" % (
            mobile_site.domain,
            self.abs_url
        )
        self.assertRaises(AppError, self.get, self.main_url)
