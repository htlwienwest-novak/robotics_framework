# TelemetryBroker for Inter Process Communication for Robtics
# MASTERNODE => THE BRAIN
# Developed by Martin Novak at 2025/26

from libs.lib_telemtrybroker import TelemetryBroker
import time

mb = TelemetryBroker() 

ROTATION_SPEED = 100
DRIVE_SPEED = 100

direction_count_left = 0
direction_count_right = 0
last_direction = "front"

mb.set("tool_pen", 1)
sensor_dict = {"sensor_distance_front":0, "sensor_distance_right":0, "sensor_distance_back":0, "sensor_distance_left":0, "sensor_angular_z":0, "sensor_linear_x":0}
#, "sensor_floor_color":"none", "sensor_victim_color":"none", "sensor_victim_letter":"none"}
aktor_dict = {"vel_linear_x":0, "vel_angular_z":0}

while True:
    sensor_dict =mb.getmulti(sensor_dict.keys())

    # 1. analyze_walls => wall_state = {"front":True, "right":True, "back":True, "left":True}
    wall_state = {"front":False, "right":False, "back":False, "left":False}
    if sensor_dict["sensor_distance_front"] < 20:
        wall_state["front"] = True
    if sensor_dict["sensor_distance_right"] < 20:
        wall_state["right"] = True
    if sensor_dict["sensor_distance_back"] < 20:
        wall_state["back"] = True
    if sensor_dict["sensor_distance_left"] < 20:
        wall_state["left"] = True

    print(wall_state)
    #time.sleep(5)

    # 3. decide_drive_direction => drive_direction
    current_angle = sensor_dict["sensor_angular_z"]
    target_angle=0
    if wall_state["left"] == False and direction_count_left < 4:
        drive_direction = "left"
        target_angle = current_angle-90
    elif wall_state["front"] == False:
        drive_direction = "front"
        target_angle = current_angle
    elif wall_state["right"] == False and direction_count_right < 4:
        drive_direction = "right"
        target_angle = current_angle+90
    elif wall_state["back"] == False:
        drive_direction = "back"
        target_angle = current_angle+180

    if last_direction == "left":
        direction_count_left += 1
    else:
        direction_count_left = 0

    if last_direction == "right":
        direction_count_right += 1
    else:
        direction_count_right = 0

    last_direction = drive_direction

    if target_angle < 0:
        target_angle += 360
    if target_angle >= 360:
        target_angle -= 360

    # 8. drive_rotation => until angle
    if drive_direction == "right" or drive_direction == "back":
        mb.set("vel_angular_z", ROTATION_SPEED)
    elif drive_direction == "left":
        mb.set("vel_angular_z", -ROTATION_SPEED)
    else:
        mb.set("vel_angular_z", 0)

    while True:
        sensor_dict = mb.getmulti(sensor_dict.keys())
        print(drive_direction, sensor_dict['sensor_angular_z'], target_angle, direction_count_left, direction_count_right)
        if sensor_dict["sensor_angular_z"] == target_angle:
            mb.set("vel_angular_z", 0)
            break


    # 9. drive_next => until next tile
    mb.set("vel_linear_x", DRIVE_SPEED)
    while True:
        sensor_dict = mb.getmulti(sensor_dict.keys())
        print(drive_direction, sensor_dict["sensor_linear_x"], target_angle, direction_count_left, direction_count_right)
        if sensor_dict["sensor_linear_x"] >= 30:
            mb.set("vel_linear_x", 0)
            break
        if sensor_dict["sensor_distance_front"] < 15:
            mb.set("vel_linear_x", 0)
            break




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

mb.close()
