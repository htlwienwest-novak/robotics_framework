# TelemetryBroker for Inter Process Communication for Robtics
# Node as Remote Control via Console
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os

mb = TelemetryBroker()

vel_dict = {"vel_linear_x":0, "vel_angular_z":0, "tool_pen":0, "led_blink":0}


CURSOR_UP_LEFT = "\033[H"  # Springt nach ganz oben links (Home)
HIDE_CURSOR = "\033[?25l"  # Versteckt den blinkenden Cursor (optional)
SHOW_CURSOR = "\033[?25h"  # Zeigt ihn wieder an

print(HIDE_CURSOR, end="") # Cursor verstecken für besseren Look

while True:
    try:
        #time.sleep(0.1)
        data = mb.getall()
        output = ""
        os.system('cls' if os.name == 'nt' else 'clear')
        for key, value in sorted(data.items()):
            output = output + f"{key}"+" : "+value+"\n"
        
        print(f"{CURSOR_UP_LEFT}{output}", end="\r", flush=True)

    except KeyboardInterrupt:
        print(SHOW_CURSOR)
        break

mb.close()
