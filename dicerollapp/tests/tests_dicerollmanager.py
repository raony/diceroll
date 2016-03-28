from django.test import override_settings, TestCase
from dicerollapp.models import DiceRollManager

@override_settings(CACHES = { 'default' :
        {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',}})
class DiceRollManagerTest(TestCase):
    def test_create(self):
        target = DiceRollManager()
        result = target.create('test description')
        self.assertIsNotNone(result.GUID)
        self.assertEqual('test description', result.description)

        result_db = target.get(result.GUID)
        self.assertEqual(result.description, result_db.description)

    def test_create_many(self):
        target = DiceRollManager()
        result1 = target.create('test description')
        result2 = target.create('test description2')

        self.assertEqual(result1.description, target.get(result1.GUID).description)
        self.assertEqual(result2.description, target.get(result2.GUID).description)