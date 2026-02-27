import time
from smbus2 import SMBus

# I2C Adresse des GY-33
ADDR = 0x5A

# Register Definitionen (laut Datenblatt)
REG_RGB_START = 0x05  # Start-Register für R, G, B Daten
REG_LUX = 0x11        # Register für Helligkeit

bus = SMBus(1) # Bus 1 beim Raspberry Pi 5

def read_color():
    try:
        # Lese 3 Bytes ab Register 0x05 (Rot, Grün, Blau)
        data = bus.read_i2c_block_data(ADDR, REG_RGB_START, 3)
        r = data[0]
        g = data[1]
        b = data[2]
        
        # Lese Helligkeit (Lux) - oft 2 Bytes
        lux_data = bus.read_i2c_block_data(ADDR, REG_LUX, 2)
        lux = (lux_data[0] << 8) | lux_data[1]
        
        return r, g, b, lux
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        return None

print("GY-33 Farbmessung gestartet...")

try:
    while True:
        result = read_color()
        if result:
            r, g, b, lux = result
            print(f"R: {r:3} | G: {g:3} | B: {b:3} | Helligkeit: {lux} lux")
            
            # Optional: Einfache Farberkennung
            if r > g and r > b:
                print("Dominante Farbe: ROT")
            elif g > r and g > b:
                print("Dominante Farbe: GRÜN")
            elif b > r and b > g:
                print("Dominante Farbe: BLAU")
                
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMessung beendet.")