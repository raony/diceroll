from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.test import override_settings

import mock
import pickle

from dicerollapp.models import DiceRoll, DiceRollManager


class HomeTest(WebTest):
    def test_display_new_diceroll_form_on_home(self):
        response = self.app.get(reverse('home'))
        self.assertIsNotNone(response.form)

    @mock.patch('redis.from_url')
    def test_form_submit(self, redis):
        pickled_result = []
        guid_result = []
        def set_stub(guid, pickled_obj):
            pickled_result.append(pickled_obj)
            guid_result.append(guid)
        DiceRollManager.get_manager().redis.set.side_effect = set_stub

        response = self.app.get(reverse('home'))
        response.form['description'] = 'test description'
        response = response.form.submit()

        DiceRollManager.get_manager().redis.set.assert_called_with(mock.ANY, mock.ANY)
        DiceRollManager.get_manager().redis.get.return_value = pickled_result[0]

        response = response.follow()

        DiceRollManager.get_manager().redis.get.assert_called_with(guid_result[0])
        self.assertContains(response, 'test description')

    def test_form_submit_empty_error(self):
        response = self.app.get(reverse('home'))
        response.form['description'] = ''
        response = response.form.submit()
        self.assertFormError(response, 'form', 'description', u'This field is required.')

@mock.patch('redis.from_url')
class DiceRollViewTest(WebTest):
    def test_get_view(self, redis):
        roll = DiceRoll('description test')
        DiceRollManager.get_manager().redis.get.return_value = pickle.dumps(roll)
        response = self.app.get(reverse('diceroll', kwargs={'id': roll.GUID}))
        DiceRollManager.get_manager().redis.get.assert_called_with(roll.GUID)

    def test_get_not_found(self, redis):
        DiceRollManager.get_manager().redis.get.return_value = None
        response = self.app.get(reverse('diceroll', kwargs={'id': 'guid'}), status=404)

    def test_post_roll(self, redis):
        roll = DiceRoll('description test')
        DiceRollManager.get_manager().redis.get.return_value = pickle.dumps(roll)
        result = {}
        def stub_set(guid, pickled_obj):
            result['guid'] = guid
            result['pickled_obj'] = pickled_obj
        DiceRollManager.get_manager().redis.set.side_effect = stub_set

        response = self.app.get(reverse('diceroll', kwargs={'id': roll.GUID}))
        self.assertIsNotNone(response.form)
        response.form['dicenum'] = 10
        response = response.form.submit()

        DiceRollManager.get_manager().redis.set.assert_called_with(roll.GUID,
                                                                   result['pickled_obj'])
        DiceRollManager.get_manager().redis.get.return_value = result['pickled_obj']

        response = response.follow()

        roll = pickle.loads(result['pickled_obj'])
        self.assertEqual(1, len(roll.rolls))
        self.assertContains(response, ', '.join([unicode(v) for v in roll.rolls[0].values]))
