# TelemetryBroker for Inter Process Communication for Robtics
# MASTERNODE => THE BRAIN
# Developed by Martin Novak at 2025/26

from libs.lib_telemtrybroker import TelemetryBroker
import time, random

mb = TelemetryBroker() 

ROTATION_SPEED = 100
DRIVE_SPEED = 100
LEFT_HAND_PREFERENCE = True # if True, prefer left turns, otherwise prefer right turns
direction_count = 0 # max count of same direction in a row to avoid loops in certain maze configurations

direction_count_left = 0
direction_count_right = 0
last_direction = "front"
black_floor_detected = False

time.sleep(5) # wait for all nodes to be ready

mb.set("tool_pen", 1)
sensor_dict = {"sensor_distance_front":0, "sensor_distance_right":0, "sensor_distance_back":0, "sensor_distance_left":0, "sensor_angular_z":0, "sensor_linear_x":0, "sensor_front_color":"", "sensor_front_color_text":"", "sensor_floor_color":"", "sensor_floor_color_text":""}


while True:
    sensor_dict =mb.getmulti(sensor_dict.keys())

    # 4. analyze_floor => floor_color
    if sensor_dict["sensor_floor_color_text"] == "blue":
        # 5. do_floor_action => e.g. blue=>wait 5s
        mb.set("vel_linear_x", 0)
        mb.set("vel_angular_z", 0)
        time.sleep(5)

    # 1. analyze_walls => wall_state = {"front":True, "right":True, "back":True, "left":True}
    wall_state = {"front":False, "right":False, "back":False, "left":False}
    if sensor_dict["sensor_distance_front"] < 20 or black_floor_detected:
        wall_state["front"] = True
        black_floor_detected = False
    if sensor_dict["sensor_distance_right"] < 20:
        wall_state["right"] = True
    if sensor_dict["sensor_distance_back"] < 20:
        wall_state["back"] = True
    if sensor_dict["sensor_distance_left"] < 20:
        wall_state["left"] = True


    # 6. analyze_victims => victim_color, victim_letter
    if sensor_dict["sensor_front_color_text"] != "" and sensor_dict["sensor_front_color_text"] != "black":
        mb.set("led_blink", 1)
    # 7. do_victim_action => set rescue kits, blink led

    
    # 3. decide_drive_direction => drive_direction
    current_angle = sensor_dict["sensor_angular_z"]
    if current_angle > 85 and current_angle < 95:
        current_angle = 90
    elif current_angle > 175 and current_angle < 185:
        current_angle = 180
    elif current_angle > 265 and current_angle < 275:
        current_angle = 270
    elif current_angle > 355 or current_angle < 5:
        current_angle = 0

    target_angle=0

    direction_count += 1

    if direction_count > 10:
        # randomly prefer left or right to avoid loops in certain maze configurations
        LEFT_HAND_PREFERENCE = not LEFT_HAND_PREFERENCE
        direction_count = 0


    if LEFT_HAND_PREFERENCE:
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
    else:
        if wall_state["right"] == False and direction_count_right < 4:
            drive_direction = "right"
            target_angle = current_angle+90
        elif wall_state["front"] == False:
            drive_direction = "front"
            target_angle = current_angle
        elif wall_state["left"] == False and direction_count_left < 4:
            drive_direction = "left"
            target_angle = current_angle-90
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
        print("ROTATION to angle:", target_angle, "current_angle:", sensor_dict["sensor_angular_z"])
        if sensor_dict["sensor_angular_z"] >= target_angle-1 and sensor_dict["sensor_angular_z"] <= target_angle+1:
            mb.set("vel_angular_z", 0)
            break


    # 9. drive_next => until next tile
    mb.set("vel_linear_x", DRIVE_SPEED)
    while True:
        sensor_dict = mb.getmulti(sensor_dict.keys())
        print("DRIVE to next tile:", sensor_dict["sensor_linear_x"], "Distance:", sensor_dict["sensor_distance_front"], "Floor Color:", sensor_dict["sensor_floor_color_text"])
        if sensor_dict["sensor_linear_x"] >= 30:
            mb.set("vel_linear_x", 0)
            break
        if sensor_dict["sensor_distance_front"] < 15:
            mb.set("vel_linear_x", 0)
            break
        # Stop if black floor detected, then reverse until no black floor anymore
        if sensor_dict["sensor_floor_color_text"] == "black":
            black_floor_detected = True
            last_move = mb.get("sensor_linear_x")
            mb.set("vel_linear_x", 0)
            time.sleep(1)
            mb.set("vel_linear_x", -DRIVE_SPEED)
            while True:
                print("Reversing from black floor:", mb.get("sensor_linear_x"), mb.get("sensor_floor_color_text"))
                if mb.get("sensor_linear_x") <= -14:
                    mb.set("vel_linear_x", 0)
                    break

        if black_floor_detected:
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
