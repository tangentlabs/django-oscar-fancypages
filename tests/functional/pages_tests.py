from django.db.models import get_model
from django.core.urlresolvers import reverse

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


class TestTheWidgetCreateView(test.FancyPagesWebTest):
    is_staff = True

    def test_shows_the_correct_form_for_a_text_widget(self):
        page = self.get(
            reverse(
                'fancypages-dashboard:widget-create',
                args=(TextWidget.code(),)
            )
        )

        self.assertContains(
            page,
            '<input id="id_text" type="text" name="text" maxlength="2000" />'
        )
        self.assertContains(
            page,
            '<input type="hidden" name="display_order" id="id_display_order" />'
        )
