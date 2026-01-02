# TelemetryBroker for Inter Process Communication for Robtics
# node for GY-33 TCS34725 color detecter sensor
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#   pip install adafruit-blinka
#   pip install adafruit-circuitpython-tcs34725
from libs.lib_telemtrybroker import TelemetryBroker
import time
import board
import busio
import adafruit_tcs34725

mb = TelemetryBroker()

data_dict = {"sensor_color_floor":(0,0,0), "sensor_color_floor_lux":0, "sensor_color_floor_temp":0}


# I2C Initialisierung
i2c = busio.I2C(board.SCL, board.SDA)

# Sensor Initialisierung
# Standardadresse ist 0x29
sensor = adafruit_tcs34725.TCS34725(i2c)

# Optional: Gain (Empfindlichkeit) und Integration Time (Messdauer) einstellen
# Gain: 1x, 4x, 16x, 60x (höher = besser bei Dunkelheit)
sensor.gain = 16 
sensor.integration_time = 50 # millisekunden

print("Farbsensor TCS34725 gestartet...")

try:
    while True:
        # Rohdaten abrufen
        r, g, b, c = sensor.color_raw
        
        # Berechnete Werte (Lux und Farbtemperatur)
        lux = sensor.lux
        temp = sensor.color_temperature
        
        # Formatierte Ausgabe
        print(f"R: {r}, G: {g}, B: {b}, Clear: {c}")
        print(f"Lux: {lux:.1f} | Temp: {temp:.1f} K")
        print("-" * 20)
        
        # Daten ins TelemetryBroker schreiben
        data_dict["sensor_color_floor"] = (r, g, b)
        data_dict["sensor_color_floor_lux"] = lux
        data_dict["sensor_color_floor_temp"] = temp
        mb.setmulti(data_dict)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nBeendet.")