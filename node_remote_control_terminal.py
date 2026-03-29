# TelemetryBroker for Inter Process Communication for Robtics
# Node as Remote Control via Console
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os

mb = TelemetryBroker()

data_dict = {}
num = 0
key_list = []

while True:
    try:
        #time.sleep(0.5)
        data = mb.getall()
        os.system('cls' if os.name == 'nt' else 'clear')
        key_list = []
        num = 0
        
        for key, value in sorted(data.items()):
            if key.startswith("node_") or key.startswith("_node_"):
                continue
            key_list.append(key)
            print(f"{num:>2}  :  {key:<30}{value}")
            num += 1
        print()
        print("ENTER => REFRESH ALL DATA")

        # INPUT
        input_key = input("keyname or number: ")

        if input_key == "":
            continue

        input_val = input("value: ")

        if input_key.isdigit():
            input_key = key_list[int(input_key)]

        data_dict[input_key] = input_val
        mb.setmulti(data_dict)

    except KeyboardInterrupt:
        break

mb.close()