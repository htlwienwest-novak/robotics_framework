# TelemetryBroker for Inter Process Communication for Robtics
# node for BNO055 orientation and psoition sensor
# sensor system with 3 sensors: Accelerometer, Gyroscope, Magnetometer
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#   pip install adafruit-blinka
#   pip install adafruit-circuitpython-bno055
from libs.lib_telemtrybroker import TelemetryBroker
import time
import board
import busio
from adafruit_bno055 import BNO055_I2C

mb = TelemetryBroker()

data_dict = {"sensor_angular_z":0, "sensor_angular_y":0, "sensor_angular_x":0, 
               "sensor_linear_x":0, "sensor_linear_y":0, "sensor_linear_z":0,
               "sensor_calibration_sys":0, "sensor_calibration_mag":0}

# Wir müssen manuell den Bus 3 definieren, da 'board.I2C()' Bus 1 nimmt
from adafruit_blinka.microcontroller.bcm2835 import pin
import adafruit_blinka.microcontroller.generic_linux.i2c as i2c

# Workaround um auf den Software-I2C Bus (/dev/i2c-3) zuzugreifen
# Alternativ: Einfach SMBus nutzen, aber CircuitPython ist komfortabler.
# Der einfachste Weg für CircuitPython auf Custom Bus:
from bitbangio import I2C as BitBangI2C

# Achtung: CircuitPython nutzt Board-Pin-Namen
# SDA = GPIO 23, SCL = GPIO 24
i2c_bus3 = busio.I2C(board.D24, board.D23) # SCL, SDA

sensor = BNO055_I2C(i2c_bus3)

while True:
    angular = sensor.euler
    linear = sensor.linear_acceleration
    sys_cal, gyro_cal, accel_cal, mag_cal = sensor.calibration_status

    data_dict["sensor_angular_x"] = angular[0]
    data_dict["sensor_angular_y"] = angular[1]
    data_dict["sensor_angular_z"] = angular[2]
    data_dict["sensor_linear_x"] = linear[0]
    data_dict["sensor_linear_y"] = linear[1]
    data_dict["sensor_linear_z"] = linear[2]
    data_dict["sensor_calibration_sys"] = sys_cal
    data_dict["sensor_calibration_mag"] = mag_cal
    mb.sendmulti(data_dict)
    #print("Euler Angle: {}".format(sensor.euler))
    #print("Linear Acceleration: {}".format(sensor.linear_acceleration))
    #print("Gravity: {}".format(sensor.gravity))

    # Kalibrierungs-Info ausgeben
    print(f"Kalibrierung (0-3): Sys={sys_cal} Mag={mag_cal}")
    print("-" * 30)

    time.sleep(0.5)