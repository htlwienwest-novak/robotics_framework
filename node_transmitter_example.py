# TelemetryBroker for Inter Process Communication for Robtics
# Client for Transmitter Nodes
# Developed by Martin Novak at 2025/26
import random
from libs.lib_telemtrybroker import TelemetryBroker

mb = TelemetryBroker() 

keys = ["vel_linear_x", "vel_linear_y", "vel_linear_z", "vel_angular_x", "vel_angular_y", "vel_angular_z"]

while True:
    try:
        for k in keys:
            val = random.randint(0, 100)
            mb.set(k, val)

            print(k,val)

    except KeyboardInterrupt:
        break

