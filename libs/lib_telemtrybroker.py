# TelemetryBroker for Inter Process Communication for Robtics
# REDIS-Wrapper
# Developed by Martin Novak at 2025

import redis
import sys
from pathlib import Path
import json

#HOST = "10.42.0.1"
HOST = "localhost"

class TelemetryBroker:
    # Constructor
    #   cache_name  - name of the cache (hash) in redis
    #   host        - redis server host
    #   port        - redis server port
    #   db          - redis database number
    def __init__(self):
        self.__r = redis.Redis(host=HOST, port=6379, db=0, decode_responses=True)
        self.__nodename = None
        self.__register_node()

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
    def type_validator_get(self, value):
        if value is None:
            return None
        if len(value) == 0:
            return None
        if value[0] == '{' and value[-1] == '}' or value[0] == '[' and value[-1] == ']':
            return json.loads(value)
        cvalue = value.replace('-', '', 1)
        if cvalue.isdigit():
            return int(value)
        if cvalue.replace('.', '', 1).isdigit():
            return float(value)
        return value

    # Validate and casting
    #   value    - input as string
    def type_validator_set(self, value):
        if value is None:
            return None
        if type(value) == bool:
            value = int(value)
        elif type(value) == dict or type(value) == list or type(value) == tuple:
            value = json.dumps(value)
        return value


    # Register current node in redis
    def __register_node(self):
        self.__nodename = Path(sys.argv[0]).stem
        print("register node:",self.__nodename)
        self.__r.set(self.__nodename, 1)

    # Set value in the cache
    #   name    - key name
    #   value   - value to set
    def set(self, name, value):
        self.__r.set(name, self.type_validator_set(value))

    # Get value from the cache
    #   name    - key name
    def get(self, name):
        return self.type_validator_get(self.__r.get(name))

    # Set multi key-value paris to cache
    #   dict    - dictionary
    def setmulti(self, dict):
        if len(dict) == 0:
            return
        
        for k,v in dict.items():
                
                dict[k] = self.type_validator_set(v)

        self.__r.mset(dict)

    # Get multi key-value pairs from the cache
    #   keys    - list of keys
    def getmulti(self, keys):
        rec_list = self.__r.mget(keys)
        for c in range(len(keys)):
            rec_list[c] = self.type_validator_get(rec_list[c])
        return dict(zip(keys, rec_list))
    
    # Get all key-value pairs from redis db
    def getall(self):
        all_keys = []
        for key in self.__r.scan_iter(match="*"):
            all_keys.append(key)
            
        return self.getmulti(all_keys)

    # Get all key-value pairs that starts with
    def getallStartsWith(self, text):
        all_keys = []
        for key in self.__r.scan_iter(match=text):
            all_keys.append(key)
            
        return self.getmulti(all_keys)
    
    # Delete key
    #   key    - key name   
    def delkey(self, key):
        self.__r.delete(key)
    


