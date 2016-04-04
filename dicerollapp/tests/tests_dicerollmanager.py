from django.test import override_settings, TestCase
from dicerollapp.models import DiceRollManager
import mock
import pickle

class DiceRollManagerTest(TestCase):
    def test_create(self):
        redis = mock.MagicMock()
        target = DiceRollManager(redis)

        result = target.create('test description')
        redis.set.assert_called_with(result.GUID, pickle.dumps(result))

        redis.get.return_value = pickle.dumps(result)
        self.assertIsNotNone(result.GUID)
        self.assertEqual('test description', result.description)

        result_db = target.get(result.GUID)
        self.assertEqual(result.description, result_db.description)

    def test_create_many(self):
        redis = mock.MagicMock()

        target = DiceRollManager(redis)
        result1 = target.create('test description')
        redis.set.assert_called_with(result1.GUID, pickle.dumps(result1))

        result2 = target.create('test description2')
        redis.set.assert_called_with(result2.GUID, pickle.dumps(result2))

        redis.get.side_effect = [
            pickle.dumps(result1),
            pickle.dumps(result2)
        ]

        self.assertEqual(result1.description, target.get(result1.GUID).description)
        self.assertEqual(result2.description, target.get(result2.GUID).description)

    def test_save(self):
        redis = mock.MagicMock()

        target = DiceRollManager(redis)
        roll = target.create('test d')
        roll.description = 'test description'
        roll.roll(5)
        target.save(roll)
        redis.set.assert_called_with(roll.GUID, pickle.dumps(roll))

        redis.get.return_value = pickle.dumps(roll)

        db_roll = target.get(roll.GUID)
        self.assertEqual(db_roll.description, roll.description)
        self.assertEqual(db_roll.rolls[0].values, roll.rolls[0].values)

    def test_iter(self):
        redis = mock.MagicMock()

        target = DiceRollManager(redis)

        redis.scan_iter.return_value = [1, 2, 3, 4, 5]

        self.assertEqual([1, 2, 3, 4, 5], [x for x in target.keys()])