from django.db.models import get_model
from django.core.urlresolvers import reverse

from fancypages import test

Page = get_model('fancypages', 'Page')
Category = get_model('catalogue', 'Category')
PageType = get_model('fancypages', 'PageType')


class TestAStaffMember(test.FancyPagesWebTest):
    is_staff = True

    def test_can_create_a_new_toplevel_article_page(self):
        page = self.get(reverse('fp-dashboard:page-list'))
        page = page.click("Create new page")

        self.assertContains(page, "Create new page")

        create_form = page.form
        create_form['name'] = "A new page"
        page = create_form.submit()

        self.assertRedirects(page, reverse('fp-dashboard:page-list'))
        page = page.follow()

        article_page = Page.objects.get(category__name="A new page")
        # we use the default template for this page with only has one
        # container
        self.assertEquals(article_page.containers.count(), 1)

        self.assertEquals(article_page.status, Page.DRAFT)
        self.assertEquals(article_page.is_visible, False)
        self.assertContains(page, u"not visible")

    def test_can_delete_an_article(self):
        Page.add_root(name="A new page")
        self.assertEquals(Page.objects.count(), 1)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete")

        page.forms['page-delete-form'].submit()
        self.assertEquals(Page.objects.count(), 0)

    def test_can_cancel_the_delete_of_a_page(self):
        Page.add_root(name="A new page")

        self.assertEquals(Page.objects.count(), 1)

        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete")
        page = page.click('cancel')
        self.assertEquals(Page.objects.count(), 1)
        self.assertContains(page, "Create new page")
        self.assertContains(page, "Page Management")

    def test_can_delete_a_child_page(self):
        parent_page = Page.add_root(name="A new page")

        p = Page.objects.get(id=parent_page.id)
        self.assertEquals(p.category.numchild, 0)

        Page.add_root(name="Another page")
        parent_page.add_child(name="The child")

        p = Page.objects.get(id=parent_page.id)
        self.assertEquals(p.category.numchild, 1)

        self.assertEquals(Page.objects.count(), 3)
        page = self.get(reverse("fp-dashboard:page-list"))
        page = page.click("Delete", index=1)

        page.forms['page-delete-form'].submit()
        self.assertEquals(Page.objects.count(), 2)
        self.assertEquals(Category.objects.count(), 2)

        p = Page.objects.get(id=parent_page.id)
        self.assertEquals(p.category.numchild, 0)
        parent_page = Page.objects.get(id=parent_page.id)

        Page.add_root(name="3rd page")
        self.assertEquals(Page.objects.count(), 3)
