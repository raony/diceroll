from django_webtest import WebTest
from django.core.urlresolvers import reverse

class HomeTest(WebTest):
    def test_display_new_diceroll_form_on_home(self):
        response = self.app.get(reverse('home'))
        self.assertEqual(response.status_int, 200)
        self.assertIsNotNone(response.form)

    def test_form_submit(self):
        response = self.app.get(reverse('home'))
        response.form['description'] = 'test description'
        response = response.form.submit()
        self.fail('to be implemented')