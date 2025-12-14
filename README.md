# Installation:
1. Install redis server on linux:
	sudo apt update
	sudo apt upgrade
	sudo apt install redis-server
	sudo systemctl start redis
	sudo systemctl enable redis
2. Install redis client libraries for python:
	pip install redis
3. Copy robotics framework on desktop:
	/home/pi/desktop/robotics_framework/
3. Install starter.py for autostart on boot:
	sudo nano ~/.config/autostart/nodestarter.desktop
   Insert following lines and correct Exec path to framework path:
       [Desktop Entry]
       Type=Application
       Name=Node Starter
       Exec=python3 /home/pi/desktop/robotics_framework/starter.py
       Terminal=true