# TelemetryBroker for Inter Process Communication for Robtics
# Installer script
# Developed by Martin Novak at 2025/26

import time
import os

pip_install_robot = [
    "redis",
    "gpiozero",
    "opencv-python",
    "numpy",
    "flask",
    "smbus2",
    "rpi_ws281x"
    "adafruit-blinka",
    "adafruit-circuitpython-busdevice",
    "adafruit-circuitpython-neopixel",
    "adafruit-circuitpython-pca9685",
    "adafruit-circuitpython-servokit",
    "adafruit-circuitpython-vl53l4cd",
    "adafruit-circuitpython-bno08x",
    "pygame",
    "matplotlib",
    "pmw3901",
    "spidev",
    "openpyxl",
    "psutil",
    "rich",
]

pip_install_remote = [
    "redis",
    "matplotlib",
    "numpy",
    "rich"
]

pip_install_sim = [
    "redis",
    "rich",
    "openpyxl",
    "scipy",
    "shapely",
    "pygame"
]


try:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Installation of Robotics Framework")
    if os.name == 'posix':
        print("Linux System detected!")
    elif os.name == 'nt':
        print("Windows System detected!")
    else:
        print("Unknown OS")
        exit()
    system = input("Destination System (1 => Fully Robot, 2 => Remote only, 3 => Simulation only):")
    if system == "1":
        for lib in pip_install_robot:
            if os.name == 'posix':
                os.system(f"pip install {lib} --break-system-packages")
            elif os.name == 'nt':
                os.system(f"pip install {lib}")
            else:
                print("Unknown OS")
    if system == "2":
        for lib in pip_install_remote:
            if os.name == 'posix':
                os.system(f"pip install {lib} --break-system-packages")
            elif os.name == 'nt':
                os.system(f"pip install {lib}")
            else:
                print("Unknown OS")
    if system == "3":
        for lib in pip_install_sim:
            if os.name == 'posix':
                os.system(f"pip install {lib} --break-system-packages")
            elif os.name == 'nt':
                os.system(f"pip install {lib}")
            else:
                print("Unknown OS")

    
    print("Installation Completed")
except KeyboardInterrupt:
    print("Installation Aborted")



