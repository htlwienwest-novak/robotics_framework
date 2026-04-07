# Installation:
## 1. Install redis server on linux:
```
sudo apt update
sudo apt upgrade
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```
Redis is used only for communication (ipc) between nodes and not for storing data.
Disable persisence of redis db.
It protects the hard drive or SD card from damage.

Change redis config to disable writing on hd or sd and allow remote connections:
```
sudo nano /etc/redis/redis.conf
```
change or append the following settings in redis.conf:
```
save ""
appendonly no
bind 0.0.0.0
protected-mode no
```
Restart redis:
```
sudo systemctl restart redis
```
## 2. Install redis client libraries for python:
```
pip install redis
```
## 3. Install starter.py for autostart on boot:
```
sudo nano ~/.config/autostart/nodestarter.desktop
```
   Insert following lines and correct Exec path to framework path:
```
[Desktop Entry]
Type=Application
Name=Node Starter
Exec=python3 /home/robot/robotics_framework/starter.py
Terminal=true
```
---
# Helper Scripts:
- control_center.py
   Easy enable or disable nodes
   Easy start enabled nodes
   Easy stop running nodes
   Easy show live data
   Easy manipulate data via console
   Easy install libraries
- starter.py
   Starts all enabled nodes:
      Enabled nodes are nodes that begin with node_*
      All nodes with a different starting name, e.g., __node_*, are disabled.
      Used as starter sript at boot

---
# Node Description:
All nodes are optimized for Raspberry Pi 4 and 5.
Not hardware specific nodes also running on Windows 

# node_master
The Brain. Master-Node for controlling system for autonomous driving.
includes the state machine for controlling the robot.
## requirements
```
Nothing
```

# node_camera_with_ocr
Node for camera sensor for recognition colors and letters H, S, U with OCR-Framework
## requirements
```
pip install easyocr
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```
## used keys
- sensor_camera_color => (R, G, B)
- sensor_camera_letter => H, S, U
## wiring diagram
|Camera|Pi|
|:---|:---|
|USB or CSI|USB or CSI|

# node_camera_without_ocr
Node for camera sensor for recognition colors and letters H, S, U with image-mapping
## requirements
```
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```
## used keys
- sensor_camera_color => (0, 0, 0) to (255,255,255)
- sensor_camera_letter => H, S, U
## wiring diagram
|Camera|Pi|
|:---|:---|
|USB or CSI|USB or CSI|

# node_motor_control_mecanum
Node for Motor Control for 4 Motors with Mecanum Wheels
## requirements
```
pip install gpiozero
```
## used keys
- vel_linear_x => -100 to 100
- vel_linear_y => -100 to 100
- vel_angular_z => -100 to 100
## wiring diagram
|Motor Controller|Pi|
|:---|:---|
|IN1|Digital Pin (PWM)|
|IN2|Digital Pin (PWM)|
|IN3|Digital Pin (PWM)|
|IN4|Digital Pin (PWM)|
|GND|GND and Battery-|
|5V|3.3V or 5V|
|12V|Battery+|

# node_motor_control
Node for Motor Control for 2 Motors (left and right)
## requirements
```
pip install gpiozero
```
## used keys
- vel_linear_x => -100 to 100
- vel_angular_z => -100 to 100
## wiring diagram
|Motor Controller|Pi|
|:---|:---|
|IN1|Digital Pin (PWM)|
|IN2|Digital Pin (PWM)|
|IN3|Digital Pin (PWM)|
|IN4|Digital Pin (PWM)|
|GND|GND and Battery-|
|5V|3.3V or 5V|
|12V|Battery+|

# node_remote_control_ps4
node for ps4 remote controller via bluetooth
## requirements
```
pip install pygame
```
## used keys
- vel_linear_x => -100 to 100
- vel_linear_y => -100 to 100
- vel_angular_z => -100 to 100
- tool_pen => 0 or 1
- led_blink => 0 or 1

# node_remote_control_terminal
node for remote control via terminal
## requirements
```
nothing
```
## used keys
all keys

# node_remote_display_terminal
node for displaying all keys in redis db
## requirements
```
nothing
```
## used keys
all keys

# node_sensor_color_floor_gy33
node for GY-33 TCS34725 color detecter sensor via i2c
## requirements
```
pip install adafruit-blinka
pip install adafruit-circuitpython-tcs34725
```
## used keys
- sensor_color_floor => (0,0,0) to (255,255,255)
- sensor_color_floor_calibrate => 1
- sensor_color_floor_text => text of color (e.g. red, green, blue)
## wiring diagram
|Color Sensor|Pi|
|:---|:---|
|VCC|3.3V|
|GND|GND|
|DR|SDA|
|CT|SCL|

Use DR/CT instead of SDL/SCL on Sensor for I2C.
Soldering S0 to GND for I2C Mode of GY33

# node_sensor_distance_lidar_vl53l4cd
node for VL53L4CD lidar distance sensors ia i2c
## requirements
```
pip install adafruit-blinka
pip install adafruit-circuitpython-vl53l4cd
```
## used keys
- sensor_distance_front => distance in mm
- sensor_distance_right => distance in mm
- sensor_distance_back => distance in mm
- sensor_distance_left => distance in mm
## wiring diagram
|Lidar Sensor|Pi|info|
|:---|:---||
|VIN|3.3V||
|GND|GND||
|SDA|SDA||
|SCL|SCL||
|XSHUT|Digital Output|for multisensor only|

XSHUT is necessery for multisensor, it's turn off sensor for programming I2C address

# node_sensor_distance_360
node for Slamtec RPLidar C1 360 distance sensors via USB
## requirements
```
nothing
```
## used keys
- sensor_distance_360 => Dictionary => degree:distance => e.g. {0:20, 1:34, 3:12, .....}
## wiring diagram
|RPLidar C1|Pi|
|:---|:---|
|USB|USB|

# node_sensor_distance_360_vis
Visualition for node_sensor_distance_360
Can also be used remotly
## requirements
```
pip install matplotlib
pip install numpy
```
## used keys
- sensor_distance_360

# node_sensor_orientation_floor_pmw3901
node for PMW3901 orientation flow sensor via spi
## requirements
```
pip install pmw3901 spidev
```
## used keys
- sensor_linear_abs_x => absolute distance
- sensor_linear_abs_y => absolute distance
## wiring diagram
|PWM3901|Pi|info|
|:---|:---||
|3V3|3V3||
|GND|GND||
|MOSI|MOSI||
|MISO|MISO||
|SCLK|SCLK||
|CS|Digital Output|for multisensor only|

working range 80mm to infinity

# node_sensor_orientation_bno08x
node for BNO08x orientation and psoition sensor via i2c
## requirements
```
pip install adafruit-blinka
pip install adafruit-circuitpython-bno08x
```
## used keys
- sensor_angular_abs_z => absolute degrees 0 to 359
- sensor_angular_abs_y => absolute degrees 0 to 359
- sensor_angular_abs_x => absolute degrees 0 to 359
- sensor_linear_rel_x => relative distance
- sensor_linear_rel_y => relative distance
- sensor_linear_rel_z => relative distance
## wiring diagram
|BNO08x|Pi|
|:---|:---|
|3V3|3V3|
|GND|GND|
|SDA|SDA|
|SCL|SCL|

# node_servo_control_16x
Node for Servo Control via 16 channel PWM Driver i2c
## requirements
```
pip install adafruit-circuitpython-servokit
```
## used keys
- servo_0 to servo_15 => 0 to 180
## wiring diagram
|PWM Driver|Pi|info|
|:---|:---||
|VCC|3V3|logic voltage|
|GND|GND||
|SDA|SDA||
|SCL|SCL||
|5V|5V Battery+|motor voltage|
|GND|Battery-||

# node_sim_maze
node for simulation of maze gametable
Creating maps with file maps.xlsx.
Use MS Excel as editor
## requirements
```
pip install openpyxl
pip install pygame
```
## used keys
- sensor_angular_z
- sensor_linear_x
- sensor_distance_front
- sensor_distance_right
- sensor_distance_left
- sensor_distance_back
- sensor_front_color
- sensor_floor_color
- vel_linear_x
- vel_angular_z
- tool_pen
- led_blink

# node_neopixel
Node for neopixel rgb led stripes
## requirements
```
pip install adafruit-blinka
pip install rpi_ws281x adafruit-circuitpython-neopixel
```
## used keys
- neopixel_color => (R, G, B)
- neopixel_blink => 0 or 1
## wiring diagram
|PWM Driver|Pi|
|:---|:---|
|5V|5V|
|GND|GND|
|Data|Digital Output|

# node_http_server
Node for recieving requests with key and value data
POST or GET Requests are possible:
GET: http://robotip:5000?key=value
POST: http://robotip:5000/ with JSON in body
## requirements
```
pip install flask
```
## used keys
- all available keys

# node_system_operations
Node for doing system commands on linux
e.g. reboot, shutdown,...
it can be triggerd remotely over network
## used keys
- reboot => 1
- shutdown => 1

# node_remote_control_keyboard
Node for remote steering via keyboard from another computer
## requirements
```
pip install pynput
```
## used keys
- vel_linear_x
- vel_linear_y
- vel_angular_z
- tool_pen
- led_blink

# node_esp
Node for ESP8266/ESP32 as Client
Communication about WIFI and Redis
## used keys
- all available keys

# Android Remote App
Remote steering app for android
node_http_server is necessary for communication

