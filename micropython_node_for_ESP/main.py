import redis
import wlan
from ulib_telemtrybroker import TelemetryBroker

SSID = "robot"
PASSWORD = "robot4ever"
HOST = "10.42.0.1"

wifi = wlan.WLAN(SSID, PASSWORD)
wifi.connect()

mb = TelemetryBroker()

while True:
    try:
        pass     # HIER KOMMT GET UND SET 

    except KeyboardInterrupt:
        print("Programm beendet")
    except:
        continue
