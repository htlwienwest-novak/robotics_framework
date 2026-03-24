# TelemetryBroker for Inter Process Communication for Robtics
# node for GY-33 TCS34725 color detecter sensor
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#    pip install smbus2
from libs.lib_telemtrybroker import TelemetryBroker
import smbus2
import time

mb = TelemetryBroker()

data_dict = {"sensor_floor_color":"(0,0,0)", "sensor_floor_color_lux":0, "sensor_floor_color_text":""}

# I2C-Adresse des GY-33
GY33_ADDRESS = 0x5A

# Register-Definitionen
REG_RED   = 0x0C
REG_GREEN = 0x0D
REG_BLUE  = 0x0E
REG_LUX_H = 0x0F
REG_LUX_L = 0x10
REG_CT_H  = 0x11
REG_CT_L  = 0x12

# I2C Bus initialisieren (Port 1 beim Raspberry Pi 5)
bus = smbus2.SMBus(1)


def calibrate_white():
    print("Starte Weißabgleich...")
    try:
        # Der Befehl 0xAD löst beim GY-33 oft die interne Kalibrierung aus
        # Manche Versionen benötigen die Sequenz 0xA5, 0xAD, Checksumme
        bus.write_byte_data(GY33_ADDRESS, 0x00, 0xAD) 
        time.sleep(2) # Dem Sensor Zeit zum Berechnen geben
        mb.set("sensor_color_floor_calibrate", "0")
        print("Weißabgleich abgeschlossen.")
    except Exception as e:
        print(f"Fehler bei Kalibrierung: {e}")


try:
    while True:

        if mb.get("sensor_color_floor_calibrate") == "1":
            calibrate_white()

        # 8-Bit RGB Werte lesen
        red = bus.read_byte_data(GY33_ADDRESS, REG_RED)
        green = bus.read_byte_data(GY33_ADDRESS, REG_GREEN)
        blue = bus.read_byte_data(GY33_ADDRESS, REG_BLUE)
        
        total = red + green + blue
        print(total)
        if total < 60: # Diesen Schwellenwert je nach Licht anpassen
            textcolor = "black"
        elif total > 100:
            textcolor = "white"
        elif red > green and red > blue and green < blue:
            textcolor = "red"
        elif blue > red and blue > green:
            textcolor = "blue"
        elif red > blue and green > blue and green > blue:
            textcolor = "yellow"
        elif green > red and green > blue:
            textcolor = "green"
        else:
            textcolor = ""

        # 16-Bit Lux berechnen (High Byte verschieben + Low Byte)
        lux_h = bus.read_byte_data(GY33_ADDRESS, REG_LUX_H)
        lux_l = bus.read_byte_data(GY33_ADDRESS, REG_LUX_L)
        lux = (lux_h << 8) | lux_l
        
        # 16-Bit Farbtemperatur (CT) berechnen
        ct_h = bus.read_byte_data(GY33_ADDRESS, REG_CT_H)
        ct_l = bus.read_byte_data(GY33_ADDRESS, REG_CT_L)
        ct = (ct_h << 8) | ct_l

        data_dict["sensor_floor_color"] = (red,green,blue)
        data_dict["sensor_floor_color_lux"] = lux
        data_dict["sensor_floor_color_text"] = textcolor
        mb.setmulti(data_dict)

        print(data_dict)

        #print(f"R: {red}, G: {green}, B: {blue} | "
        #          f"Helligkeit: {lux} lux | "
        #          f"Farbtemp: {ct} K")
        
        time.sleep(0.5)  # Kurze Pause zwischen den Messungen


except KeyboardInterrupt:
    print("\nProgramm beendet.")
except Exception as e:
    print(f"Fehler beim Lesen: {e}")


"""

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
"""