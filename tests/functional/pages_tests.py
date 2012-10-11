from django.db.models import get_model
from django.core.urlresolvers import reverse

from django_dynamic_fixture import get as G

from fancypages import test

Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')
TextWidget = get_model('fancypages', 'TextWidget')
TitleTextWidget = get_model('fancypages', 'TitleTextWidget')


class TestAStaffMember(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.article_type = PageType.objects.create(name='Article', code='article',
                                template_name=self.template_name)
        self.other_type = PageType.objects.create(name='Other', code='other',
                                                  template_name="")

        self.prepare_template_file(
            "{% load fancypages_tags%}"
            "{% fancypages-container first-container %}"
            "{% fancypages-container second-container %}"
        )

    def test_can_see_a_list_of_page_types(self):
        page = self.get(reverse('fancypages-dashboard:page-list'))

        self.assertContains(page, 'Article')
        self.assertContains(page, 'Other')

    def test_can_create_a_new_toplevel_article_page(self):
        page = self.get(reverse('fancypages-dashboard:page-list'))

        type_form = page.form
        type_form['page_type'] = self.article_type.code
        page = type_form.submit()

        self.assertRedirects(
            page,
            reverse(
                'fancypages-dashboard:page-create',
                args=(self.article_type.code,)
            ),
            status_code=301
        )
        page = page.follow()
        self.assertContains(page, "Create new 'Article' page")

        create_form = page.form
        create_form['title'] = "A new page"
        page = create_form.submit()

        self.assertRedirects(page, reverse('fancypages-dashboard:page-list'))
        page = page.follow()

        article_page = Page.objects.get(title="A new page")
        self.assertEquals(article_page.containers.count(), 2)

        self.assertEquals(article_page.status, Page.DRAFT)
        self.assertEquals(article_page.is_visible, False)
        self.assertContains(page, u"not visible")


class TestAWidget(test.FancyPagesWebTest):

    def setUp(self):
        super(TestAWidget, self).setUp()
        self.page_type = PageType.objects.create(name='Article', code='article',
                                                 template_name=self.template_name)
        self.prepare_template_file(
            "{% load fancypages_tags%}"
            "{% fancypages-container main-container %}"
        )

        self.page = Page.objects.create(
            title="A new page",
            code='a-new-page',
            page_type=self.page_type,
        )

        self.text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('main-container'),
            text="some text",
            display_order=0,
        )

        self.second_text_widget = TextWidget.objects.create(
            container=self.page.get_container_from_name('main-container'),
            text="second text",
            display_order=1,
        )

    def test_can_be_deleted(self):
        page = self.get(reverse(
            'fancypages-dashboard:widget-delete',
            args=(self.second_text_widget.id,)
        ))
        # we need to fake a body as the template does not
        # contain that
        page.body = "<body>%s</body>" % page.body
        page = page.form.submit()

        self.assertEquals(TextWidget.objects.count(), 1)
        self.assertRaises(
            TextWidget.DoesNotExist,
            TextWidget.objects.get,
            id=self.second_text_widget.id
        )

    def test_can_be_deleted_and_remaining_widgets_are_reordered(self):
        pass
