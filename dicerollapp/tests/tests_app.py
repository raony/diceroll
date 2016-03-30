from django_webtest import WebTest
from django.core.urlresolvers import reverse

from dicerollapp.models import DiceRoll

class HomeTest(WebTest):
    def test_display_new_diceroll_form_on_home(self):
        response = self.app.get(reverse('home'))
        self.assertEqual(response.status_int, 200)
        self.assertIsNotNone(response.form)

    def test_form_submit(self):
        response = self.app.get(reverse('home'))
        response.form['description'] = 'test description'
        response = response.form.submit()
        response = response.follow()

        self.assertContains(response, 'test description')

    def test_form_submit_empty_error(self):
        response = self.app.get(reverse('home'))
        response.form['description'] = ''
        response = response.form.submit()
        self.assertFormError(response, 'form', 'description', u'This field is required.')

def 