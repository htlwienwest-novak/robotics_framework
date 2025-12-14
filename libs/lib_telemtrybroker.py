# TelemetryBroker for Inter Process Communication for Robtics
# REDIS-Wrapper
# Developed by Martin Novak at 2025

import redis
import os
import sys
from pathlib import Path

class TelemetryBroker:
    # Constructor
    #   cache_name  - name of the cache (hash) in redis
    #   host        - redis server host
    #   port        - redis server port
    #   db          - redis database number
    def __init__(self, cache_name="botcom", host="localhost", port=6379, db=0):
        self._r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self._cache_name = cache_name
        self.clear()
        self._value_cache = {}
        self._nodename = None
        self._register_node()
        self._cb_keys = []
        self._cb_function = ""

    # Destructor
    def __del__(self):
        self._r.close()

    # Register current node in redis
    def _register_node(self):
        self._nodename = Path(sys.argv[0]).stem
        print("register node:",self._nodename)
        self._r.hsetnx(self._cache_name, self._nodename, 1)

    # Set other node activation state
    def set_other_node_activation(self, nodename, value):
        self.set(nodename, int(value))

    # Check activation state from node
    def is_active_node(self):
        return bool(self._r.hget(self._cache_name, self._nodename))

    # Set value in the cache
    #   name    - key name
    #   value   - value to set
    def set(self, name, value):
        if not self.is_active_node():
            return
        self._r.hset(self._cache_name, name, value)

    # Get value from the cache
    #   name    - key name
    def get(self, name):
        if not self.is_active_node():
            return None
        return self._r.hget(self._cache_name, name)

    # Get all key-value pairs from the cache
    def getall(self):
        if not self.is_active_node():
            return None
        return self._r.hgetall(self._cache_name)

    # Clear the cache
    def clear(self):
        self._r.delete(self._cache_name)

    # Set callback function for keys
    #   keys    - list of key names to monitor
    #   cbfunc  - callback function to call on value change
    def setcallback(self, keys, cbfunc):
        self._cb_keys = keys
        self._cb_function = cbfunc

    # Checks messages from redis
    def receiver_loop(self):
        while True:
            if not self.is_active_node():
                continue
            for item in self._cb_keys:
                val = self.get(item)
                if val is None:
                    continue
                if item not in self._value_cache:
                    self._value_cache[item] = val
                    continue
                for k,v in self._value_cache.items():
                    if item == k and val != v:
                        self._value_cache[item] = self.get(item)
                        self._cb_function(item, val)

