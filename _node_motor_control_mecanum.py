# TelemetryBroker for Inter Process Communication for Robtics
# Node for Motor Control for 4 Motors with Mecanum Wheels
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

# Die Pin-Nummern sind GPIO Nummern:
m_lf = DCMotor(5, 6)  # left front 
m_rf = DCMotor(23, 24)  # right front
m_lb = DCMotor(12, 16)  # left back
m_rb = DCMotor(25, 13)  # right back

vel_dict = {"vel_linear_x":0, "vel_linear_y":0, "vel_angular_z":0}

while True:
    try:
        #print(vel_dict)
        vel_dict = mb.getmulti(vel_dict.keys())

        if vel_dict is None:
            continue
        if vel_dict["vel_linear_x"] is None or vel_dict["vel_linear_y"] is None or vel_dict["vel_angular_z"] is None:
            continue

        vel_linear_x = int(vel_dict["vel_linear_x"])
        vel_linear_y = int(vel_dict["vel_linear_y"])
        vel_angular_z = int(vel_dict["vel_angular_z"])

        # Vorwärts oder rückwärts:
        if vel_linear_x != 0 and vel_linear_y == 0 and vel_angular_z == 0:
            print("vorwärts/rückwärts")
            m_lf.drive(vel_linear_x)
            m_rf.drive(vel_linear_x)
            m_lb.drive(vel_linear_x)
            m_rb.drive(vel_linear_x)

        # Seitwärts rechts oder links
        elif vel_linear_x == 0 and vel_linear_y != 0 and vel_angular_z == 0:
            print("seitwärts")
            m_lf.drive(vel_linear_y)
            m_rf.drive(-vel_linear_y)
            m_lb.drive(-vel_linear_y)
            m_rb.drive(vel_linear_y)

        # Drehung nach rechts oder links:
        elif vel_linear_x == 0 and vel_linear_y == 0 and vel_angular_z != 0:
            print("drehen")
            m_lf.drive(vel_angular_z)
            m_rf.drive(-vel_angular_z)
            m_lb.drive(vel_angular_z)
            m_rb.drive(-vel_angular_z)

        # Kurvenfahrt:
        elif vel_linear_x != 0 and vel_linear_y == 0 and vel_angular_z != 0:
            print("kurve")
            pass
        
        # STOP:
        else:
            print("stop")
            m_lf.drive(0)
            m_rf.drive(0)
            m_lb.drive(0)
            m_rb.drive(0)

    except KeyboardInterrupt:
        m_lf.drive(0)
        m_rf.drive(0)
        m_lb.drive(0)
        m_rb.drive(0)
        break

mb.close()

