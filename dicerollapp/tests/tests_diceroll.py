from unittest import TestCase
from dicerollapp.models import DiceRoll
import mock

class DiceRollTest(TestCase):
    def test_new(self):
        target = DiceRoll('test description')
        self.assertIsNotNone(target.GUID)
        self.assertEqual('test description', target.description)
        self.assertEqual(0, len(target.rolls))

    @mock.patch('random.randint')
    def test_roll(self, random_call):
        results = [1, 4, 7, 8, 6, 9]
        random_call.side_effect = results

        target = DiceRoll('test description')
        target.roll(6)

        self.assertEqual(1, len(target.rolls))
        self.assertEqual(results, target.rolls[0].values)
        self.assertEqual(2, target.rolls[0].successes())

    @mock.patch('random.randint')
    def test_roll(self, random_call):
        results = [1, 10, 10, 8, 10, 9]
        random_call.side_effect = results

        target = DiceRoll('test description')
        target.roll(3)

        self.assertEqual(1, len(target.rolls))
        self.assertEqual(results, target.rolls[0].values)