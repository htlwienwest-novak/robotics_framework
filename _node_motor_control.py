# TelemetryBroker for Inter Process Communication for Robtics
# Node for Motor Control for 2 Motors left/right
# Developed by Martin Novak at 2025/26

import RPi.GPIO as GPIO
from libs.lib_telemtrybroker import TelemetryBroker

class Motor:
    def __init__(self, pwmpin1, pwmpin2, direction=True):
        GPIO.setmode(GPIO.BCM)  # Wir nutzen die GPIO-Nummern (nicht die Pin-Nummern)
        GPIO.setup(pwmpin1, GPIO.OUT)
        GPIO.setup(pwmpin2, GPIO.OUT)
        pwm_objekt = GPIO.PWM(18, 1000)
        self.pwmpin1 = GPIO.PWM(pwmpin1, 1000)
        self.pwmpin2 = GPIO.PWM(pwmpin2, 1000)
        self.pwmpin1.start(0)
        self.pwmpin2.start(0)
        self.direction = direction

    def drive(self, value):
        #Setze RIchtung -100 bis 100
        self.pwmpin1.start(0)
        self.pwmpin2.start(0)

        if not self.direction:
            value = -value

        if value==0:
            self.pwmpin1.ChangeDutyCycle(0)
            self.pwmpin2.ChangeDutyCycle(0)
        elif value>=0:
            self.pwmpin1.ChangeDutyCycle(int(abs(value)))
            self.pwmpin2.ChangeDutyCycle(0)
        else:
            self.pwmpin1.ChangeDutyCycle(0)
            self.pwmpin2.ChangeDutyCycle(int(abs(value)))
        
mb = TelemetryBroker()
m1 = Motor(12, 13) 
m2 = Motor(19, 26)

vel_dict = {"vel_linear_x":0, "vel_angular_z":0}

while True:
    try:
        print(vel_dict)
        vel_dict = mb.getmulti(vel_dict.keys())

        if vel_dict["vel_linear_x"] != 0 and vel_dict["vel_angular_z"] == 0:
            m1.drive(vel_dict["vel_linear_x"])
            m2.drive(vel_dict["vel_linear_x"])
        elif vel_dict["vel_linear_x"] == 0 and vel_dict["vel_angular_z"] != 0:
            if vel_dict["vel_angular_z"] > 0:
                m1.drive(vel_dict["vel_angular_z"])
                m2.drive(-vel_dict["vel_angular_z"])
            elif vel_dict["vel_angular_z"] < 0:
                m1.drive(-vel_dict["vel_angular_z"])
                m2.drive(vel_dict["vel_angular_z"])
            else:
                m1.drive(0)
                m2.drive(0)
        else:
            m1.drive(0)
            m2.drive(0)

    except KeyboardInterrupt:
        break

mb.close()
GPIO.cleanup()
