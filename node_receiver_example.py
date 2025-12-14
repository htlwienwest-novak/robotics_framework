# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time

mb = TelemetryBroker()

def cb_getmessage(key, value):
    print("CALLBACK:", key, value)


keys = ["vel_linear_x", "vel_linear_y", "vel_linear_z", "vel_angular_x", "vel_angular_y", "vel_angular_z"]
mb.setcallback(keys, cb_getmessage)


while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break



"""

x1_cache = None
x2_cache = None 
x3_cache = None

while True:
    try:
        x1 = mb.get("sensor1")
        x2 = mb.get("sensor2")
        x3 = mb.get("sensor3")

        if x1 != x1_cache or x2 != x2_cache or x3 != x3_cache:
            print(x1,x2,x3)

            x1_cache = x1
            x2_cache = x2
            x3_cache = x3

    except KeyboardInterrupt:
        break
"""