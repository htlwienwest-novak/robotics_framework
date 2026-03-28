# TelemetryBroker for Inter Process Communication for Robtics
# node for VL53L4CD distance sensors
# sensor system with 4 sensors: front, right, left, back
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#   pip install adafruit-blinka
#   pip install adafruit-circuitpython-vl53l4cd
from libs.lib_telemtrybroker import TelemetryBroker

import time
import board
import busio
from adafruit_vl53l4cd import VL53L4CD
from gpiozero import LED


mb = TelemetryBroker()

data_dict = {"sensor_distance_front":0, "sensor_distance_right":0, "sensor_distance_back":0, "sensor_distance_left":0}
xshut_pins = [4, 17, 27, 22]  # Wir nutzen hier GPIO 4, 17, 27, 22
sensor_list = []
base_address = 0x30  # Startadresse für die Sensoren (0x30, 0x31, 0x32, 0x33)

# I2C Bus initialisieren
i2c = board.I2C()

# Addressierung aller Sensoren über XSHUT Pins (Reset)
# Alle Sensoren ausschalten:
xshut_obj = []

for pin in xshut_pins:
    xshut = LED(pin)
    xshut.off()  # Sensor ausschalten (Low)
    xshut_obj.append(xshut)

    
time.sleep(0.1)  # Kurz warten, bis Sensor gebootet hat

# Alle Sensoren nacheinander einschalten und neue Adresse vergeben
for i, xshut in enumerate(xshut_obj):
    # a) Sensor einschalten
    xshut.on()  # Sensor einschalten (High) 
    time.sleep(0.1) # Kurz warten, bis Sensor gebootet hat
    
    # b) Sensor auf Standard-Adresse 0x29 initialisieren
    sensor = VL53L4CD(i2c)
    
    # c) Adresse ändern! (WICHTIG)
    new_address = base_address + i
    sensor.set_address(new_address)
    
    # d) Sensor konfigurieren und zur Liste hinzufügen
    sensor.inter_measurement = 0
    sensor.timing_budget = 50
    sensor.start_ranging()
    sensor_list.append(sensor)


print("VL53L4CD Messung gestartet...")


try:
    while True:
        for i, vl53 in enumerate(sensor_list):
            vl53.start_ranging()
            if vl53.data_ready:
                # Messung löschen für den nächsten Durchgang
                vl53.clear_interrupt()
                
                # Distanz in cm umrechnen (Sensor gibt mm aus)
                distance = int(vl53.distance * 10)

                if i == 0:  # front
                    data_dict["sensor_distance_front"] = distance
                elif i == 1:  # right
                    data_dict["sensor_distance_right"] = distance
                elif i == 2:  # back
                    data_dict["sensor_distance_back"] = distance
                elif i == 3:  # left
                    data_dict["sensor_distance_left"] = distance    

            mb.setmulti(data_dict)
            #print(data_dict)
            
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\nMessung beendet.")

"""
import time
import board
import busio
from digitalio import DigitalInOut, Direction
from adafruit_vl53l4cd import VL53L4CD

mb = TelemetryBroker()

data_dict = {"sensor_distance_front":0, "sensor_distance_right":0, "sensor_distance_back":0, "sensor_distance_left":0}


# 1. Definition der XSHUT Pins (passe diese an deine Verkabelung an)
# Wir nutzen hier GPIO 4, 17, 27, 22
# Reihenfolge der Sensoren: [front, right, back, left]
xshut_pins = [board.D4, board.D17, board.D27, board.D22]

xshut_gpios = []
sensors = []

# 2. XSHUT Pins vorbereiten und alle Sensoren AUSschalten (Reset)
for pin in xshut_pins:
    gpio = DigitalInOut(pin)
    gpio.direction = Direction.OUTPUT
    gpio.value = False # Sensor ausschalten (Low)
    xshut_gpios.append(gpio)

print("Alle Sensoren im Reset-Modus...")
time.sleep(0.1) 

# 3. I2C Bus initialisieren
i2c = busio.I2C(board.SCL, board.SDA)

# 4. Sensoren nacheinander einschalten und neue Adresse vergeben
# Wir starten bei Adresse 0x30, um Konflikte mit dem Standard 0x29 zu vermeiden
base_address = 0x30 

for i, gpio in enumerate(xshut_gpios):
    # a) Sensor einschalten
    gpio.value = True
    time.sleep(0.1) # Kurz warten, bis Sensor gebootet hat
    
    # b) Sensor auf Standard-Adresse 0x29 initialisieren
    sensor = VL53L4CD(i2c)
    
    # c) Adresse ändern! (WICHTIG)
    new_address = base_address + i
    sensor.set_address(new_address)
    
    # d) Sensor konfigurieren und zur Liste hinzufügen
    sensor.inter_measurement = 0
    sensor.timing_budget = 50
    sensor.start_ranging()
    sensors.append(sensor)
    
    print(f"Sensor {i+1} initialisiert an Adresse 0x{new_address:02x}")

print("---------------------------")
print("Messung läuft...")

try:
    while True:
        results = []
        for i, sensor in enumerate(sensors):
            # Prüfen ob Daten da sind (wir warten hier nicht blockierend, sondern überspringen ggf.)
            if sensor.data_ready:
                sensor.clear_interrupt()
                dist = sensor.distance
                results.append(f"S{i+1}: {dist:5.1f} cm")
                if i == 0:  # front
                    data_dict["sensor_distance_front"] = dist
                elif i == 1:  # right
                    data_dict["sensor_distance_right"] = dist
                elif i == 2:  # back
                    data_dict["sensor_distance_back"] = dist
                elif i == 3:  # left
                    data_dict["sensor_distance_left"] = dist
            else:
                results.append(f"S{i+1}: --.- cm")
        
        # Alle Ergebnisse in einer Zeile ausgeben
        print(" | ".join(results))
        # Daten ins TelemetryBroker schreiben
        mb.setmulti(data_dict)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStoppe Messungen...")
    for sensor in sensors:
        sensor.stop_ranging()

"""