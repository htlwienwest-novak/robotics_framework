# TelemetryBroker for Inter Process Communication for Robtics
# Node for Motor Control for 2 Motors left/right
# Developed by Martin Novak at 2025/26

from gpiozero import Motor
from libs.lib_telemtrybroker import TelemetryBroker

class DCMotor:
    def __init__(self, pwmpin1, pwmpin2, direction=True):
        self.motor = Motor(pwmpin1, pwmpin2)    #, enable=22)
        self.motor.stop()
        self.direction = direction

    def drive(self, value):
        #Setze RIchtung -100 bis 100
        speed = abs(value/100)

        if value==0:
            self.motor.stop()
        elif value>0:
            self.motor.forward(speed)
        else:
            self.motor.backward(speed)
        
mb = TelemetryBroker()
m1 = DCMotor(12, 13) 
m2 = DCMotor(19, 26)

vel_dict = {"vel_linear_x":0, "vel_angular_z":0}

while True:
    try:
        #print(vel_dict)
        vel_dict = mb.getmulti(vel_dict.keys())

        if vel_dict is None:
            continue
        if vel_dict["vel_linear_x"] is None or vel_dict["vel_angular_z"] is None:
            continue

        vel_linear_x = int(vel_dict["vel_linear_x"])
        vel_angular_z = int(vel_dict["vel_angular_z"])

        # Vorwärts:
        if vel_linear_x != 0 and vel_angular_z == 0:
            print("vorwärts/rückwärts")
            m1.drive(vel_linear_x)
            m2.drive(vel_linear_x)

        # Drehung:
        elif vel_linear_x == 0 and vel_angular_z != 0:
            print("drehen")
            m1.drive(vel_angular_z)
            m2.drive(-vel_angular_z)

        # Kurvenfahrt:
        elif vel_linear_x != 0 and vel_angular_z != 0:
            print("kurve")
            pass

        # STOP:
        else:
            print("stop")
            m1.drive(0)
            m2.drive(0)

    except KeyboardInterrupt:
        m1.drive(0)
        m2.drive(0)
        break

mb.close()

