from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages import test

Page = get_model('fancypages', 'Page')
PageType = get_model('fancypages', 'PageType')
PageTemplate = get_model('fancypages', 'PageTemplate')


class TestAStaffMember(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.article_type = PageType.objects.create(
            name='Article',
            code='article',
            template=self.template
        )
        empty_template = PageTemplate.objects.create(
            title="empty",
            description="empty",
            template_name=""
        )
        self.other_type = PageType.objects.create(name='Other', code='other',
                                                  template=empty_template)

        self.prepare_template_file(
            "{% load fp_container_tags%}"
            "{% fancypages-container first-container %}"
            "{% fancypages-container second-container %}"
        )

    def test_can_see_a_list_of_page_types(self):
        page = self.get(reverse('fp-dashboard:page-list'))

        self.assertContains(page, 'Article')
        self.assertContains(page, 'Other')

    def test_can_create_a_new_toplevel_article_page(self):
        page = self.get(reverse('fp-dashboard:page-list'))

        type_form = page.form
        type_form['page_type'] = self.article_type.code
        page = type_form.submit()

        self.assertRedirects(
            page,
            reverse(
                'fp-dashboard:page-create',
                args=(self.article_type.code,)
            ),
            status_code=301
        )
        page = page.follow()
        self.assertContains(page, "Create new 'Article' page")

        create_form = page.form
        create_form['title'] = "A new page"
        page = create_form.submit()

        self.assertRedirects(page, reverse('fp-dashboard:page-list'))
        page = page.follow()

        article_page = Page.objects.get(title="A new page")
        self.assertEquals(article_page.containers.count(), 2)

        self.assertEquals(article_page.status, Page.DRAFT)
        self.assertEquals(article_page.is_visible, False)
        self.assertContains(page, u"not visible")

    def test_can_delete_an_article(self):
        Page.add_root(
            title="A new page",
            page_type=self.article_type,
        )
        self.assertEquals(Page.objects.count(), 1)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete")

        page.forms['page-delete-form'].submit()
        self.assertEquals(Page.objects.count(), 0)

    def test_can_cancel_the_delete_of_a_page(self):
        Page.add_root(
            title="A new page",
            page_type=self.article_type,
        )
        self.assertEquals(Page.objects.count(), 1)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete")
        page = page.click('cancel')
        self.assertEquals(Page.objects.count(), 1)
        self.assertContains(page, "Create new page")
        self.assertContains(page, "Page Management")

    def test_can_delete_a_child_page(self):
        parent_page = Page.add_root(
            title="A new page",
            page_type=self.article_type,
        )
        self.assertEquals(Page.objects.get(id=parent_page.id).numchild, 0)
        Page.add_root(
            title="Another page",
            page_type=self.article_type,
        )

        parent_page.add_child(
            title="The child",
            page_type=self.article_type,
        )
        self.assertEquals(Page.objects.get(id=parent_page.id).numchild, 1)

        self.assertEquals(Page.objects.count(), 3)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete", index=1)

        page.forms['page-delete-form'].submit()
        self.assertEquals(Page.objects.count(), 2)

        self.assertEquals(Page.objects.get(id=parent_page.id).numchild, 0)
        parent_page = Page.objects.get(id=parent_page.id)

        Page.add_root(
            title="3rd page",
            page_type=self.article_type,
        )
        self.assertEquals(Page.objects.count(), 3)


class TestAPageTemplate(test.FancyPagesWebTest):
    is_staff = True

    def test_are_listed_in_the_dashboard(self):
        page = self.app.get(
            reverse('fp-dashboard:page-template-list'),
            user=self.user
        )
        self.assertContains(page, self.template.title)
        self.assertContains(page, self.template.description)
        self.assertContains(page, self.template.template_name)

        self.assertContains(
            page,
            reverse(
                'fp-dashboard:page-template-update',
                args=(self.template.id,)
            )
        )
        self.assertContains(
            page,
            reverse(
                'fp-dashboard:page-template-delete',
                args=(self.template.id,)
            )
        )

    def test_cannot_be_created_with_template_does_not_exist(self):
        page = self.app.get(
            reverse('fp-dashboard:page-template-list'),
            user=self.user
        )
        page = page.click('Create new page template')

        self.assertEquals(PageTemplate.objects.count(), 1)

        template_form = page.form
        template_form['title'] = "Added template"
        template_form['description'] = 'The added description'
        template_form['template_name'] = 'a/sample/template/file.html'
        page = template_form.submit()

        self.assertContains(
            page,
            "template %s does not exist" % 'a/sample/template/file.html'
        )

    def test_can_be_created_without_image_in_the_dashboard(self):
        page = self.app.get(
            reverse('fp-dashboard:page-template-list'),
            user=self.user
        )
        page = page.click('Create new page template')

        self.assertEquals(PageTemplate.objects.count(), 1)

        template_form = page.form
        template_form['title'] = "Added template"
        template_form['description'] = 'The added description'
        template_form['template_name'] = self.template_name
        page = template_form.submit()

        self.assertRedirects(
            page,
            reverse('fp-dashboard:page-template-list')
        )

        self.assertEquals(PageTemplate.objects.count(), 2)

        template = PageTemplate.objects.get(title="Added template")
        self.assertEquals(template.description, 'The added description')
        self.assertEquals(template.template_name, self.template_name)

    def test_can_be_updated_without_image_in_the_dashboard(self):
        page = self.app.get(
            reverse('fp-dashboard:page-template-list'),
            user=self.user
        )
        page = page.click('Edit')

        self.assertContains(page, 'Update page template')

        template_form = page.form
        template_form['title'] = "new title"
        page = template_form.submit()

        self.assertRedirects(
            page,
            reverse('fp-dashboard:page-template-list')
        )

        self.assertEquals(PageTemplate.objects.count(), 1)

        template = PageTemplate.objects.get(id=self.template.id)
        self.assertEquals(template.title, 'new title')

    def test_can_be_deleted_in_the_dashboard(self):
        page = self.app.get(
            reverse('fp-dashboard:page-template-list'),
            user=self.user
        )
        self.assertEquals(PageTemplate.objects.count(), 1)
        page = page.click('Delete')

        self.assertContains(page, 'Delete page template')

        template_form = page.form
        page = template_form.submit()

        self.assertRedirects(
            page,
            reverse('fp-dashboard:page-template-list')
        )

        self.assertEquals(PageTemplate.objects.count(), 0)
