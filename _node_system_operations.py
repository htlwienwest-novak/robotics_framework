# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import subprocess
import os

mb = TelemetryBroker()

datadict = {"reboot":0, "shutdown":0}


def get_ip_address(interface='eth0'):
    try:
        # Führt den Befehl 'ip -4 addr show eth0' aus
        output = subprocess.check_output(['ip', '-4', 'addr', 'show', interface]).decode('utf-8')
        
        # Sucht nach der Zeile mit 'inet' und extrahiert die IP
        for line in output.split('\t'):
            if 'inet ' in line:
                return line.split()[1].split('/')[0]
    except Exception as e:
        return ""

ip_eth0 = get_ip_address("eth0")
if ip_eth0 != "":
    datadict["ip"] = ip_eth0
    print(f"Ethernet IP: {ip_eth0}")    

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
