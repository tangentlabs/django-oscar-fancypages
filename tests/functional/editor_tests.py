from django.core.urlresolvers import reverse

from shawn.testcases import ZombieTestCase


class TestOnAFancyPage(ZombieTestCase):
    is_staff = True

    #def test_content_can_be_added_by_staff_member(self):
    #    browser = self.get(reverse('basket:summary'))
    #    self.assertContains(browser, 'Your saved basket is empty')
    #    self.assertContains(browser, 'Add content')

    #    browser = self.browser.clickLink('Add content')
    #    self.assertContains(browser, 'widget_code')

    #    browser = browser.client.wait('fire', 'click', "input[value='text']")
    #    print browser.body.html

    #def test_clicking_edit_on_a_widget_loads_settings(self):
    #    print self.browser.body.html
