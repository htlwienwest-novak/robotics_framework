# TelemetryBroker for Inter Process Communication for Robtics
# node for ultrasonic HC-SR04 distance sensors
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#   pip install gpiozero

from libs.lib_telemtrybroker import TelemetryBroker

from gpiozero import DistanceSensor
import time

mb = TelemetryBroker()

data_dict = {"sensor_distance_front":0, "sensor_distance_right":0, "sensor_distance_back":0, "sensor_distance_left":0}

sensor_front = DistanceSensor(echo=18, trigger=17)
sensor_back = DistanceSensor(echo=18, trigger=17)
sensor_left = DistanceSensor(echo=18, trigger=17)
sensor_right = DistanceSensor(echo=18, trigger=17)

try:
    while True:
        distance_front = sensor_front.distance * 100
        distance_back = sensor_back.distance * 100
        distance_left = sensor_left.distance * 100
        distance_right = sensor_right.distance * 100
        
        data_dict["sensor_distance_front"] = distance_front
        data_dict["sensor_distance_back"] = distance_back
        data_dict["sensor_distance_left"] = distance_left
        data_dict["sensor_distance_right"] = distance_right
        
        print('Distance: ', distance_front, distance_back, distance_left, distance_right)
        mb.setmulti(data_dict)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMessung beendet.")
    mb.close()
