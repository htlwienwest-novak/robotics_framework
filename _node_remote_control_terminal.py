# TelemetryBroker for Inter Process Communication for Robtics
# Node as Remote Control via Console
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os

mb = TelemetryBroker()

data_dict = {}

while True:
    try:
        #time.sleep(0.5)
        data = mb.getall()
        os.system('cls' if os.name == 'nt' else 'clear')
        for key, value in sorted(data.items()):
            print(f"{value:>5}", ":", key)
        print()

        # INPUT
        input_key = input("key:")
        input_val = input("val:")

        if input_key == "" or input_val == "":
            continue

        data_dict[input_key] = input_val
        mb.setmulti(data_dict)

    except KeyboardInterrupt:
        break

mb.close()