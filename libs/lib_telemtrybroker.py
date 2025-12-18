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

    # Validate and casting
    #   value    - input as string
    def type_validator(self, value):
        cvalue = value.replace('-', '', 1)
        if cvalue.isdigit():
            return int(value)
        if cvalue.replace('.', '', 1).isdigit():
            return float(value)
        return value

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
        if isinstance(value, bool):
            value = int(value)
        self._r.set(name, value)

    # Get value from the cache
    #   name    - key name
    def get(self, name):
        if not self.is_active_node():
            return None
        return self.type_validator(self._r.get(name))

    # Set multi key-value paris to cache
    #   dict    - dictionary
    def setmulti(self, dict):
        if len(dict) == 0:
            return
        for k,v in dict.items():
            if isinstance(v, bool):
                dict[k] = int(v)
        self._r.mset(dict)

    # Get multi key-value pairs from the cache
    #   keys    - list of keys
    def getmulti(self, keys):
        if not self.is_active_node():
            return None
        rec_list = self._r.mget(keys)
        for c in range(len(rec_list)):
            rec_list[c] = self.type_validator(rec_list[c])
        return dict(zip(keys, rec_list))
    
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

            for k, v in self.getmulti(self._cb_dict.keys()):
                if self._cb_dict[k] == v:
                    continue
                self._cb_dict[k] = v
                self._cb_function(k, v)


