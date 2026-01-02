import spidev

class ADNS3080:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 3 # ADNS3080 nutzt oft Mode 3
        
        # Sensor checken (Product ID sollte 0x17 sein)
        pid = self.read_register(0x00)
        if pid != 0x17:
            print(f"WARNUNG: ADNS3080 nicht erkannt! ID: {hex(pid)}")
        else:
            print("ADNS3080 erfolgreich erkannt.")
            
        # Konfiguration (optional): Auflösung auf 1600 cpi setzen
        # Register 0x09: Bit 4 setzen für hohe Auflösung, Bit 5A setzen
        self.write_register(0x0a, 0x10) # Configuration_bits

    def read_register(self, addr):
        # MSB muss 0 sein für Read (eigentlich Standard, aber wir senden Adresse)
        resp = self.spi.xfer2([addr, 0x00])
        return resp[1]

    def write_register(self, addr, value):
        # MSB muss 1 sein für Write
        self.spi.xfer2([addr | 0x80, value])

    def get_motion(self):
        # Liest Motion Register (0x02)
        # Wenn Bit 7 (0x80) gesetzt ist, gab es Bewegung
        motion = self.read_register(0x02)
        
        if motion & 0x80:
            # Delta X und Y lesen
            dx = self.read_register(0x03)
            dy = self.read_register(0x04)
            
            # Umwandlung in signed integer (8-bit two's complement)
            if dx > 127: dx -= 256
            if dy > 127: dy -= 256
            
            return dx, dy
        return 0, 0