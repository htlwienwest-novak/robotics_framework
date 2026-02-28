# TelemetryBroker for Inter Process Communication for Robtics
# node for PMW3901 orientation on floor
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#    sudo apt-get install python3-spidev
#    pip install pmw3901 spidev

import math
from libs.lib_telemtrybroker import TelemetryBroker
import argparse
import time

from pmw3901 import PMW3901

print("Press Ctrl+C to exit!")

ROTATION_RADIUS = 100  # Radius für Rotationsbewegungen in mm

mb = TelemetryBroker()
data_dict = {"sensor_linear_abs_x":0, "sensor_linear_abs_y":0}

flo = PMW3901(spi_cs_gpio=0)
flo.set_rotation(0)

tx = 0
ty = 0

try:
    while True:
        try:
            x, y = flo.get_motion()
        except RuntimeError:
            continue
        tx += x
        ty += y

        #angular_z = int((ty*180)/(math.pi*ROTATION_RADIUS))  # Vereinfachte Annahme für Rotation
        data_dict["sensor_linear_abs_x"] = tx
        data_dict["sensor_linear_abs_y"] = ty
        #data_dict["sensor_angular_abs_z"] = angular_z
        print(data_dict)
        mb.setmulti(data_dict)

        #print(f"Relative: x {x:03d} y {y:03d} | Absolute: x {tx:03d} y {ty:03d}")
        time.sleep(0.01)
except KeyboardInterrupt:
    mb.close()




"""
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
"""