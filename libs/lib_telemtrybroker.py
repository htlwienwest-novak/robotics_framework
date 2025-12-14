# TelemetryBroker for Inter Process Communication for Robtics
# REDIS-Wrapper
# Developed by Martin Novak at 2025

import redis

class TelemetryBroker:
    # Constructor
    #   cache_name  - name of the cache (hash) in redis
    #   host        - redis server host
    #   port        - redis server port
    #   db          - redis database number
    def __init__(self, cache_name="botcom", host="localhost", port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.cache_name = cache_name
        self.clear()
        self.value_cache = {}

    # Destructor
    def __del__(self):
        self.r.close()

    # Set value in the cache
    #   name    - key name
    #   value   - value to set
    def set(self, name, value):
        self.r.hset(self.cache_name, name, value)

    # Get value from the cache
    #   name    - key name
    def get(self, name):
        return self.r.hget(self.cache_name, name)

    # Get all key-value pairs from the cache
    def getall(self):
        return self.r.hgetall(self.cache_name)

    # Clear the cache
    def clear(self):
        self.r.delete(self.cache_name)

    # Set callback function for keys
    #   keys    - list of key names to monitor
    #   cbfunc  - callback function to call on value change
    def setcallback(self, keys, cbfunc):
        while True:
            for item in keys:
                val = self.get(item)
                if val is None:
                    continue
                if item not in self.value_cache:
                    self.value_cache[item] = val
                    continue
                for k,v in self.value_cache.items():
                    if item == k and val != v:
                        self.value_cache[item] = self.get(item)
                        cbfunc(item, val)
