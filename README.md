# Installation:
1. Install redis server on linux:
	sudo apt update
	sudo apt upgrade
	sudo apt install redis-server
	sudo systemctl start redis
	sudo systemctl enable redis
3. Install redis client libraries for python:
	pip install redis
4. Copy robotics framework on desktop:
	/home/pi/desktop/robotics_framework/
3. Install starter.py for autostart on boot:
	sudo nano ~/.config/autostart/nodestarter.desktop
   Insert following lines and correct Exec path to framework path:
       [Desktop Entry]
       Type=Application
       Name=Node Starter
       Exec=python3 /home/pi/desktop/robotics_framework/starter.py
       Terminal=true

Example Nodes:
- node_motor_control
- node_sensor_distance
- node_sensor_linear_angular
- node_sensor_color
- node_sensor_camera
- node_remote_control_ps4
- node_drive_control
- node_touchdisplay_control
- node_navigation_control

Example Key Types:
- vel_linear_x	-100 bis 100
- vel_linear_y	-100 bis 100
- vel_linear_z	-100 bis 100
- vel_angular_x	-100 bis 100
- vel_angular_y	-100 bis 100
- vel_angular_z	-100 bis 100
- move_state		0 stop, 1 drive
- mode			0 manual, 1 autonom
- sensor_range_front		cm
- sensor_range_left		cm
- sensor_range_right		cm
- sensor_range_back		cm
- sensor_linear_x
- sensor_linear_y
- sensor_linear_z
- sensor_angular_x
- sensor_angular_y
- sensor_angular_z
- sensor_angular_abs_x	0 bis 359
- sensor_angular_abs_y	0 bis 359
- sensor_angular_abs_z	0 bis 359
- map_current_position			(x,y)
- map_goal_position		(x,y)
