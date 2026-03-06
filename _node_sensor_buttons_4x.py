# TelemetryBroker for Inter Process Communication for Robtics
# Node for Buttons 4x
# Developed by Martin Novak at 2025/26

from gpiozero import Button
from libs.lib_telemtrybroker import TelemetryBroker

mb = TelemetryBroker()

vel_dict = {"sensor_button_0":0, "sensor_button_1":0, "sensor_button_2":0, "sensor_button_3":0}

button0 = Button(2)
button1 = Button(3)
button2 = Button(4)
button3 = Button(5)

while True:
    try:
        if button0.is_pressed:
            vel_dict["sensor_button_0"] = 1
        if button1.is_pressed:
            vel_dict["sensor_button_1"] = 1
        if button2.is_pressed:
            vel_dict["sensor_button_2"] = 1
        if button3.is_pressed:
            vel_dict["sensor_button_3"] = 1

        mb.setmulti(vel_dict)

    except KeyboardInterrupt:
        break

mb.close()

