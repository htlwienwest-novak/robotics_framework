# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os

mb = TelemetryBroker()

vel_dict = {"vel_linear_x":0, "vel_angular_z":0, "tool_pen":0, "led_blink":0}

while True:
    try:
        #time.sleep(0.5)
        data = mb.getall()
        os.system('cls' if os.name == 'nt' else 'clear')
        for key, value in sorted(data.items()):
            print(f"{value:>5}", ":", key)
        print()
        # INPUT
        for key, value in vel_dict.items():
            invalue = input(str(key) + ":")
            if invalue == "":
                continue
            vel_dict[key] = invalue

        mb.setmulti(vel_dict)
    except KeyboardInterrupt:
        break

mb.close()