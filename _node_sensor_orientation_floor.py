# TelemetryBroker for Inter Process Communication for Robtics
# node for BNO055 orientation and psoition sensor
# sensor system with 3 sensors: Accelerometer, Gyroscope, Magnetometer
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#    sudo apt-get install python3-spidev
import math
from libs.lib_telemtrybroker import TelemetryBroker
import time
from libs.lib_adns3080 import ADNS3080
import math

mb = TelemetryBroker()

data_dict = {"sensor_angular2_z":0, "sensor_linear2_x":0, "sensor_linear2_y":0}

ROTATION_RADIUS = 100  # Radius für Rotationsbewegungen in mm

optik_sensor = ADNS3080(bus=0, device=0)

# Variablen zum Aufsummieren der Strecke (einfache Odometrie)
pos_x = 0
pos_y = 0

try:
    while True:
        # --- ADNS3080 Auslesen ---
        dx, dy = optik_sensor.get_motion()
        
        if dx == 0 and dy == 0:
            # Keine Bewegung erkannt
            pos_x=0
            pos_y=0
            continue

        # Position aufsummieren (Pixel-Counts)
        pos_x += dx
        pos_y += dy
        angular_z = (pos_y*180)/(math.pi*ROTATION_RADIUS)  # Vereinfachte Annahme für Rotation

        # Ausgabe
        # \r sorgt dafür, dass die Zeile überschrieben wird (Live-Ansicht)
        print(pos_x, pos_y, angular_z, end='       \r')
        
        data_dict["sensor_linear2_x"] = pos_x
        data_dict["sensor_linear2_y"] = pos_y
        data_dict["sensor_angular2_z"] = angular_z
        mb.sendmulti(data_dict)

        # Kurze Pause (nicht zu lang, sonst verpasst der optische Sensor schnelle Bewegungen!)
        #time.sleep(0.05)

except KeyboardInterrupt:
    print("\nProgramm beendet.")
    optik_sensor.spi.close()