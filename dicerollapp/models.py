from __future__ import unicode_literals
import random

from django.db import models
from django.core.cache import caches
from uuid import uuid4
# Create your models here.

class DiceRollManager(object):
    def __init__(self):
        self._cache = caches['default']

    def create(self, description):
        diceroll = DiceRoll(description)
        self._cache.set(diceroll.GUID, diceroll)
        return diceroll

    def get(self, GUID):
        return self._cache.get(GUID)


class DiceRoll(object):

    class _roll(object):
        def __init__(self, values):
            self.values = values

        def successes(self):
            return len([value for value in self.values if value >= 8])

    def __init__(self, description):
        self.GUID = uuid4()
        self.description = description
        self.rolls = []

    def _roll_with_explode(self, dices):
        if not dices:
            return []
        result = [random.randint(1,10) for n in xrange(dices)]
        exploded = len([x for x in result if x == 10])
        return result + self._roll_with_explode(exploded)

    def roll(self, dices):
        self.rolls.append(DiceRoll._roll(self._roll_with_explode(dices)))
