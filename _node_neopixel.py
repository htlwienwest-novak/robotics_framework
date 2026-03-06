# TelemetryBroker for Inter Process Communication for Robtics
# node for WS2812B NeoPixel RGB LED Strip control
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#   pip install adafruit-blinka
#   pip install rpi_ws281x adafruit-circuitpython-neopixel


from libs.lib_telemtrybroker import TelemetryBroker
import board
import neopixel
import time
import math

mb = TelemetryBroker()

data_dict = {"neopixel_color":(0,0,0), "neopixel_blink":0}

# Konfiguration
LED_PIN = board.D18          # GPIO 18
LED_COUNT = 4               # Anzahl deiner LEDs
ORDER = neopixel.GRB         # Farbreihenfolge (meist GRB oder RGB)

BLINK_DURATION = 0.5        # Dauer des Blinkens in Sekunden
BLINK_COUNT = 5               # Anzahl der Blinkvorgänge

pixels = neopixel.NeoPixel(
    LED_PIN, LED_COUNT, brightness=0.2, auto_write=False, pixel_order=ORDER
)

try:
    while True:
        data_dict = mb.getmulti(data_dict.keys())
        if data_dict is None:
            continue

        if data_dict["neopixel_blink"] == 1:
            for i in range(BLINK_COUNT):
                pixels.fill(data_dict["neopixel_color"])
                pixels.show()
                time.sleep(BLINK_DURATION)
                pixels.fill((0, 0, 0))
                pixels.show()
                time.sleep(BLINK_DURATION)

            data_dict["neopixel_blink"] = 0
            mb.setmulti(data_dict)

        else:
            pixels.fill(data_dict["neopixel_color"])
            pixels.show()
            time.sleep(1)

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    mb.close()