# TelemetryBroker for Inter Process Communication for Robtics
# Node for Servo Control via 16channe PWM Driver i2c
# Developed by Martin Novak at 2025/26
# Installation:
#    pip install adafruit-circuitpython-servokit

from gpiozero import Motor
from libs.lib_telemtrybroker import TelemetryBroker
import time
from adafruit_servokit import ServoKit
        
mb = TelemetryBroker()

# Initialisierung für 16 Kanäle
kit = ServoKit(channels=16)

data_dict = {"servo_0":0}
print("SERVO PWM DRIVER started!")

while True:
    data_dict = mb.getallStartsWith("servo_*")
    #print(data_dict)
    for key, value in data_dict.items():

        try:
            nr = int(key.split("_")[1])
            my_servo = kit.servo[nr]
        
            # Optional: Setze den Pulsweitenbereich (Standard ist meist 1000-2000)
            # Viele Servos brauchen 500 bis 2500 für vollen 180° Weg
            # my_servo.set_pulse_width_range(500, 2500)
            my_servo.set_pulse_width_range(500, 2500)
            my_servo.angle = int(value)

        except KeyboardInterrupt:
            print("Programm beendet")
        except:
            continue

mb.close()

