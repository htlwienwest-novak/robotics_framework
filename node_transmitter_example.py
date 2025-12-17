# TelemetryBroker for Inter Process Communication for Robtics
# Client for Transmitter Nodes
# Developed by Martin Novak at 2025/26
import random
from libs.lib_telemtrybroker import TelemetryBroker

mb = TelemetryBroker() 

vel_dict = {"vel_linear_x":0, "vel_linear_y":0, "vel_linear_z":0, "vel_angular_x":0, "vel_angular_y":0, "vel_angular_z":0}

while True:
    try:
        for k, v in vel_dict.items():
            vel_dict[k] = random.randint(0, 100)

        print(vel_dict)
        mb.setmulti(vel_dict)

    except KeyboardInterrupt:
        break

