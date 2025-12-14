# TelemetryBroker for Inter Process Communication for Robtics
# Client for Receiver Nodes
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time

mb = TelemetryBroker()

def cb_getmessage(key, value):
    print("CALLBACK:", key, value)


keys = ["vel_linear_x", "vel_linear_y", "vel_linear_z", "vel_angular_x", "vel_angular_y", "vel_angular_z"]
mb.setcallback(keys, cb_getmessage)

mb.receiver_loop()
