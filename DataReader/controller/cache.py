import redis
from decouple import config
from datetime import date, datetime, timedelta

class Cache:
    r = redis.Redis(host = config('REDIS_HOST'), port = config('REDIS_PORT'), db = config('REDIS_DB'))

    def setCache(self, key, value):
        self.r.setex(key, timedelta(days=1), value)

    def getCache(self, key):
        return self.r.get(key)