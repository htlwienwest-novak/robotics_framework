# TelemetryBroker for Inter Process Communication for Robtics
# node for remote ps4 controler 
# Developed by Martin Novak at 2025/26
# 
# Installation:
# sudo apt install python3-dev python3-pip
# pip install pyPS4Controller
#
# Pairing PS4 Controller with Raspberry Pi:
#   sudo bluetoothctl
#   scan on
#   pair [MAC_ADDRESS]
#   connect [MAC_ADDRESS]
#   trust [MAC_ADDRESS]
#   exit

from pyPS4Controller.controller import Controller
from libs.lib_telemtrybroker import TelemetryBroker
import time


class MyController(Controller):

    def __init__(self, **kwargs):
        # Das Interface ist typischerweise /dev/input/js0
        # Prüfen Sie mit 'ls /dev/input' ob js0 existiert
        super().__init__(interface="/dev/input/js0", connecting_using_ds4drv=False, **kwargs)
        self.mb = TelemetryBroker() 

    # Beispiel-Handler für Tasten (Buttons)
    def on_x_press(self):
        print("Taste X gedrückt")

    def on_x_release(self):
        print("Taste X losgelassen")

    def on_triangle_press(self):
        print("on_triangle_press")

    def on_triangle_release(self):
        print("on_triangle_release")

    def on_circle_press(self):
        print("on_circle_press")

    def on_circle_release(self):
        print("on_circle_release")

    def on_square_press(self):
        print("on_square_press")

    def on_square_release(self):
        print("on_square_release")

    def on_L1_press(self):
        print("on_L1_press")

    def on_L1_release(self):
        print("on_L1_release")

    def on_L2_press(self, value):
        print("on_L2_press: {}".format(value))

    def on_L2_release(self):
        print("on_L2_release")

    def on_R1_press(self):
        print("on_R1_press")

    def on_R1_release(self):
        print("on_R1_release")

    def on_R2_press(self, value):
        print("on_R2_press: {}".format(value))

    def on_R2_release(self):
        print("on_R2_release")

    def on_up_arrow_press(self):
        print("on_up_arrow_press")

    def on_up_down_arrow_release(self):
        print("on_up_down_arrow_release")

    def on_down_arrow_press(self):
        print("on_down_arrow_press")

    def on_left_arrow_press(self):
        print("on_left_arrow_press")

    def on_left_right_arrow_release(self):
        print("on_left_right_arrow_release")

    def on_right_arrow_press(self):
        print("on_right_arrow_press")



    # Beispiel-Handler für Analog-Sticks
    # Die Werte liegen im Bereich von -32767 bis 32767
    def on_L3_up(self, value):
        print("on_L3_up: {}".format(value))

    def on_L3_down(self, value):
        print("on_L3_down: {}".format(value))

    def on_L3_left(self, value):
        print("on_L3_left: {}".format(value))

    def on_L3_right(self, value):
        print("on_L3_right: {}".format(value))

    def on_L3_y_at_rest(self):
        """L3 joystick is at rest after the joystick was moved and let go off"""
        print("on_L3_y_at_rest")

    def on_L3_x_at_rest(self):
        """L3 joystick is at rest after the joystick was moved and let go off"""
        print("on_L3_x_at_rest")

    def on_L3_press(self):
        """L3 joystick is clicked. This event is only detected when connecting without ds4drv"""
        print("on_L3_press")

    def on_L3_release(self):
        """L3 joystick is released after the click. This event is only detected when connecting without ds4drv"""
        print("on_L3_release")

    def on_R3_up(self, value):
        print("on_R3_up: {}".format(value))

    def on_R3_down(self, value):
        print("on_R3_down: {}".format(value))

    def on_R3_left(self, value):
        print("on_R3_left: {}".format(value))

    def on_R3_right(self, value):
        print("on_R3_right: {}".format(value))

    def on_R3_y_at_rest(self):
        """R3 joystick is at rest after the joystick was moved and let go off"""
        print("on_R3_y_at_rest")

    def on_R3_x_at_rest(self):
        """R3 joystick is at rest after the joystick was moved and let go off"""
        print("on_R3_x_at_rest")

    def on_R3_press(self):
        """R3 joystick is clicked. This event is only detected when connecting without ds4drv"""
        print("on_R3_press")

    def on_R3_release(self):
        """R3 joystick is released after the click. This event is only detected when connecting without ds4drv"""
        print("on_R3_release")

    def on_options_press(self):
        print("on_options_press")

    def on_options_release(self):
        print("on_options_release")

    def on_share_press(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_share_press")

    def on_share_release(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_share_release")

    def on_playstation_button_press(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_playstation_button_press")

    def on_playstation_button_release(self):
        """this event is only detected when connecting without ds4drv"""
        print("on_playstation_button_release")
        
    # Eine vollständige Liste der möglichen Methoden finden Sie in der pyPS4Controller-Dokumentation.


try:
    controller = MyController()
    
    print("Warte auf Controller-Eingaben... (Strg+C zum Beenden)")
    controller.listen(timeout=60) 
    
except FileNotFoundError:
    print("Controller nicht gefunden unter /dev/input/js0. Stellen Sie sicher, dass er verbunden ist.")
except Exception as e:
    print(e)
          