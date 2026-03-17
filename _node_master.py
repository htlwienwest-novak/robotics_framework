# TelemetryBroker for Inter Process Communication for Robtics
# MASTERNODE => THE BRAIN
# Developed by Martin Novak at 2025/26

from libs.lib_telemtrybroker import TelemetryBroker
import time

mb = TelemetryBroker() 

time.sleep(5) # wait for all nodes to be ready

target_angle = 0  # target angle for rotation

while True:
    # GO FORWARD WITH SPEED 100 UNTIL OBSTACLE IN FRONT IS LESS THAN 15 PIXEL
    mb.set("vel_linear_x", 100)
    while True:
        distance = mb.get("sensor_distance_front")
        print(f"Distance: {distance}")
        if distance < 15:
            break
    mb.set("vel_linear_x", 0)

    time.sleep(0.5) # wait for 0.5s

    # ROTATE WITH SPEED 100 UNTIL ANGLE IS 90 DEGREE
    target_angle += 90
    mb.set("vel_angular_z", 100)
    while True:
        angle = mb.get("sensor_angular_z")
        print(f"Angle: {angle}")
        if angle >= target_angle:
            break
    mb.set("vel_angular_z", 0)

    if target_angle >= 270:
        target_angle = 0



# One cycle from tile to tile:
# 1. analyze_walls => wall_state = {"0":True, "90":True, "180":True, "270":True}
# 2. do_mapping
# 3. decide_drive_direction => drive_direction
# 4. analyze_floor => floor_color
# 5. do_floor_action => e.g. blue=>wait 5s
# 6. analyze_victims => victim_color, victim_letter
# 7. do_victim_action => set rescue kits, blink led
# 8. drive_rotation => until angle
# 9. drive_next => until next tile
# when target tile arrived, then GOTO 1

#mb.close()
