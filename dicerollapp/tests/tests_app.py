from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.test import override_settings

import mock

from dicerollapp.models import DiceRoll


class HomeTest(WebTest):
    def test_display_new_diceroll_form_on_home(self):
        response = self.app.get(reverse('home'))
        self.assertIsNotNone(response.form)

    # @mock.patch('redis.from_url')
    # def test_form_submit(self, redis):
    #     redis.get.return_value = DiceRoll('test description')
    #
    #     response = self.app.get(reverse('home'))
    #     response.form['description'] = 'test description'
    #     response = response.form.submit()
    #     response = response.follow()
    #
    #     self.assertContains(response, 'test description')

#     def test_form_submit_empty_error(self):
#         response = self.app.get(reverse('home'))
#         response.form['description'] = ''
#         response = response.form.submit()
#         self.assertFormError(response, 'form', 'description', u'This field is required.')
#
# class DiceRollViewTest(WebTest):
#     def test_get_view(self):
#         roll = DiceRoll.manager.create('description test')
#         response = self.app.get(reverse('diceroll', kwargs={'id': roll.GUID}))
#
#     def test_get_not_found(self):
#         response = self.app.get(reverse('diceroll', kwargs={'id': 'guid'}), status=404)
#
#     def test_post_roll(self):
#         roll = DiceRoll.manager.create('description test')
#         response = self.app.get(reverse('diceroll', kwargs={'id': roll.GUID}))
#         self.assertIsNotNone(response.form)
#         response.form['dicenum'] = 10
#         response = response.form.submit()
#         response = response.follow()
#
#         roll = DiceRoll.manager.get(roll.GUID)
#         self.assertEqual(1, len(roll.rolls))
#         self.assertContains(response, ', '.join([unicode(v) for v in roll.rolls[0].values]))
