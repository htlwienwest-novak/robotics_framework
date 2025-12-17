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
    def __init__(self, host="localhost", port=6379, db=0):
        self._r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self._dict_cache = {}
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
        self._r.set(self._nodename, 1)

    # Set other node activation state
    def set_other_node_activation(self, nodename, value):
        self.set(nodename, int(value))

    # Check activation state from node
    def is_active_node(self):
        return bool(self._r.get(self._nodename))

    # Set value in the cache
    #   name    - key name
    #   value   - value to set
    def set(self, name, value):
        if not self.is_active_node():
            return
        self._r.set(name, value)

    # Get value from the cache
    #   name    - key name
    def get(self, name):
        if not self.is_active_node():
            return None
        return self._r.get(name)

    # Set multi key-value paris to cache
    #   dict    - dictionary
    def setmulti(self, dict):
        if len(dict) == 0:
            return
        self._r.mset(dict)

    # Get multi key-value pairs from the cache
    #   keys    - list of keys
    def getmulti(self, keys):
        if not self.is_active_node():
            return None
        return self._r.mget(keys)
    
    # Get all key-value pairs from redis db
    def getall(self):
        return {}

    # Set callback function for keys
    #   keys    - list of key names to monitor
    #   cbfunc  - callback function to call on value change
    def setcallback(self, keys, cbfunc):
        self._cb_dict = dict.fromkeys(keys)
        self._cb_function = cbfunc

    # Checks messages from redis
    def receiver_loop(self):
        while True:
            if not self.is_active_node():
                continue
            retrieved_values = self._r.mget(self._cb_dict.keys())

            for key, value in zip(self._cb_dict.keys(), retrieved_values):
                if self._cb_dict[key] == value:
                    continue
                self._cb_dict[key] = value
                self._cb_function(key, value)


