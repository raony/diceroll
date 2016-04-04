from __future__ import unicode_literals
import random

from django.db import models
from django.core.cache import caches
from uuid import uuid4
import os
import redis as redismodule
import pickle

class DiceRollManager(object):
    _instance = None

    @classmethod
    def get_manager(cls):
        if not cls._instance:
            cls._instance = cls(redismodule.from_url(os.environ.get("REDIS_URL")))
        return cls._instance

    def __init__(self, redis):
        self.redis = redis

    def create(self, description):
        diceroll = DiceRoll(description)
        self.save(diceroll)
        return diceroll

    def get(self, GUID):
        try:
            return pickle.loads(self.redis.get(GUID))
        except:
            return None

    def save(self, diceroll):
        return self.redis.set(diceroll.GUID, pickle.dumps(diceroll))

    def keys(self):
        for key in self.redis.scan_iter():
            yield key


class _roll(object):
    def __init__(self, values):
        self.values = values

    def successes(self):
        return len([value for value in self.values if value >= 8])

class DiceRoll(object):
    def __init__(self, description):
        self.GUID = unicode(uuid4())
        self.description = description
        self.rolls = []

    def _roll_with_explode(self, dices):
        if not dices:
            return []
        result = [random.randint(1,10) for n in xrange(dices)]
        exploded = len([x for x in result if x == 10])
        return result + self._roll_with_explode(exploded)

    def roll(self, dices):
        self.rolls.insert(0, _roll(self._roll_with_explode(dices)))