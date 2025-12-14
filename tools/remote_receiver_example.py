# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os

mb = TelemetryBroker()

while True:
    try:
        time.sleep(0.5)
        data = mb.getall()
        os.system('cls' if os.name == 'nt' else 'clear')
        for key, value in data.items():
            print(key, ":", value)
    except KeyboardInterrupt:
        break

mb.close()