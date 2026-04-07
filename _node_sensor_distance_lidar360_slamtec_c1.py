# TelemetryBroker for Inter Process Communication for Robtics
# node for Slamtec RPLidar C1 distance sensors
# sensor system with 4 sensors: front, right, left, back
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:

from libs.lib_telemtrybroker import TelemetryBroker
import serial
import time

mb = TelemetryBroker()

data_dict = {}
angle_dict = {}
measured_angles = [0, 90, 180, 270]   # Winkel Filter, nur diese Winkel werden verarbeitet

PORT = '/dev/ttyUSB0'
BAUD = 460800

def get_lidar_data():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        ser.flushInput() # Alten Puffer leeren
        
        print("Starte Scan...")
        ser.write(b'\xa5\x20') # Scan-Befehl senden
        
        # Den 7-Byte Antwort-Header überspringen (A5 5A ...)
        descriptor = ser.read(7)
        print(f"Lidar antwortet: {descriptor.hex()}")

        print("Lese Messwerte (Strg+C zum Stoppen)...")
        while True:
            # Ein Standard-Datenpunkt ist 5 Bytes lang
            raw_data = ser.read(5)
            if len(raw_data) < 5:
                continue
            
            # --- DATEN PARSEN ---
            # Byte 0: Check-Bits und Qualität
            quality = raw_data[0] >> 2
            
            # Byte 1 & 2: Winkel (wird in 1/64 Grad gesendet)
            # Wir extrahieren den Winkel und prüfen das Check-Bit
            angle_raw = (raw_data[1] >> 1) | (raw_data[2] << 7)
            angle = int(angle_raw / 64.0)
            
            # Byte 3 & 4: Distanz (Millimeter)
            # Das ist die kritische Stelle für das 65000-Problem!
            dist_raw = raw_data[3] | (raw_data[4] << 8)
            distance = int(dist_raw / 4.0) # Der C1 nutzt meist Viertel-Millimeter
            
            if measured_angles.count(angle) == 0:
                continue

            # Filtern: Nur plausible Werte anzeigen
            if distance > 0 and distance < 12000: # Max 12 Meter
                #print(f"Winkel: {angle}° | Distanz: {distance:8} mm | Qualität: {quality}")
                #data_dict["sensor_distance_"+str(angle)] = distance
                angle_dict[angle] = distance
                data_dict["sensor_distance_360"] = angle_dict
                mb.setmulti(data_dict)

    except KeyboardInterrupt:
        print("\nStoppe...")
    finally:
        ser.write(b'\xa5\x25') # Stopp-Befehl
        ser.close()

if __name__ == "__main__":
    get_lidar_data()
        
