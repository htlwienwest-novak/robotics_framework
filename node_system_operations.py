# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os

mb = TelemetryBroker()

datadict = {"reboot":0, "shutdown":0}
mb.setmulti(datadict)


while True:
    try:
        datadict = mb.getmulti(datadict.keys())
        #print(datadict)
        if datadict["reboot"] == 1:
            os.system("sudo reboot")
            break
        if datadict["shutdown"] == 1:
            os.system("sudo shutdown now")
            break

        time.sleep(3)
    except KeyboardInterrupt:
        break

mb.close()


