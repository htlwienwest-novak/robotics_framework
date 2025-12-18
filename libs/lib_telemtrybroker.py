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
        self.__r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.__cb_dict = {}
        self.__nodename = None
        self.__register_node()
        self.__cb_function = ""

    # Destructor
    def __del__(self):
        self.close()

    # Close connection to database
    def close(self):
        self.delkey(self.__nodename)
        self.__r.close()


    # Clear all data in database
    def clearall(self):
        self.__r.flushall()

    # Validate and casting
    #   value    - input as string
    def type_validator(self, value):
        if value == None:
            return None
        cvalue = value.replace('-', '', 1)
        if cvalue.isdigit():
            return int(value)
        if cvalue.replace('.', '', 1).isdigit():
            return float(value)
        return value

    # Register current node in redis
    def __register_node(self):
        self.__nodename = Path(sys.argv[0]).stem
        print("register node:",self.__nodename)
        self.__r.set(self.__nodename, 1)

    # Set other node activation state
    def set_other_node_activation(self, nodename, value):
        self.set(nodename, int(value))

    # Check activation state from node
    def is_active_node(self):
        return bool(self.__r.get(self.__nodename))

    # Set value in the cache
    #   name    - key name
    #   value   - value to set
    def set(self, name, value):
        if not self.is_active_node():
            return
        if isinstance(value, bool):
            value = int(value)
        self.__r.set(name, value)

    # Get value from the cache
    #   name    - key name
    def get(self, name):
        if not self.is_active_node():
            return None
        return self.type_validator(self.__r.get(name))

    # Set multi key-value paris to cache
    #   dict    - dictionary
    def setmulti(self, dict):
        if len(dict) == 0:
            return
        for k,v in dict.items():
            if isinstance(v, bool):
                dict[k] = int(v)
        self.__r.mset(dict)

    # Get multi key-value pairs from the cache
    #   keys    - list of keys
    def getmulti(self, keys):
        if not self.is_active_node():
            return None
        rec_list = self.__r.mget(keys)
        for c in range(len(rec_list)):
            rec_list[c] = self.type_validator(rec_list[c])
        return dict(zip(keys, rec_list))
    
    # Get all key-value pairs from redis db
    def getall(self):
        all_keys = []
        for key in self.__r.scan_iter(match="*", count=20):
            all_keys.append(key)
            
        return self.getmulti(all_keys)
    
    # Delete key
    #   key    - key name   
    def delkey(self, key):
        self.__r.delete(key)
    
    # Set callback function for keys
    #   keys    - list of key names to monitor
    #   cbfunc  - callback function to call on value change
    def setcallback(self, keys, cbfunc):
        self.__cb_dict = dict.fromkeys(keys)
        self.__cb_function = cbfunc

    # Checks messages from redis
    def receiver_loop(self):
        while True:
            if not self.is_active_node():
                continue
            rec_dict = self.getmulti(self.__cb_dict.keys())
            if rec_dict == None:
                continue
            for k, v in rec_dict.items():
                if self.__cb_dict[k] == v:
                    continue
                self.__cb_dict[k] = v
                self.__cb_function(k, v)


