import redis
from decouple import config

class Cache:
    r = redis.Redis(host = config('REDIS_HOST'), port = config('REDIS_PORT'), db = config('REDIS_DB'))

    def setCache(self, key, value):
        self.r.set(key, value)

    def getCache(self, key):
        return self.r.get(key)