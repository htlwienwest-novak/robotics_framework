# TelemetryBroker for Inter Process Communication for Robtics
# MASTERNODE => THE BRAIN
# Developed by Martin Novak at 2025/26

from libs.lib_telemtrybroker import TelemetryBroker

mb = TelemetryBroker() 

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
