# TelemetryBroker for Inter Process Communication for Robtics
# DRIVE NODE => for the controlled driving of the robot
# Developed by Martin Novak at 2025/26

from libs.lib_telemtrybroker import TelemetryBroker

mb = TelemetryBroker() 

# DRIVE STATES:
# forward => until next tile
# stop
# rotation_right => until +90 degrees
# rotation_left  => until -90 degrees
# rotation_turn  => until +180 degrees


mb.close()
