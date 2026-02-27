import spidev

for x in range(2):
    spi = spidev.SpiDev()
    spi.open(0, 0) # Bus 0, Device 0 (GPIO 8)
    spi.max_speed_hz = 2000000
    spi.mode = 0b11 # Der PMW3901 braucht oft Mode 3

    # Wir lesen Register 0x00 (Product ID)
    # Wir senden 0x00 und ein Dummy-Byte, um die Antwort zu erhalten
    answer = spi.xfer2([0x00, 0x00])
    print(f"Antwort vom Sensor (Hex): {hex(answer[1])}")

    if answer[1] == 0x49:
        print("SENSOR GEFUNDEN! Hardware-ID ist korrekt (0x49).")
    else:
        print("Keine korrekte Antwort. Verkabelung prüfen!")
    spi.close()