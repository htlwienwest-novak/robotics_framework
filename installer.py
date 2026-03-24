# TelemetryBroker for Inter Process Communication for Robtics
# Installer script
# Developed by Martin Novak at 2025/26

import time
import os

pip_install_linux = [
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
    "psutil"
]

pip_install_remote = [
    "redis",
    "matplotlib",
    "numpy"
]


try:
    print("Installation of Robotics Framework")
    system = input("Destination System (1 => Robot, 2 => Remote):")
    if os.name == 'posix':
        #LINUX:
        if system == "1":
            for lib in pip_install_linux:
                os.system(f"pip install {lib} --break-system-packages")
        if system == "2":
            for lib in pip_install_remote:
                os.system(f"pip install {lib} --break-system-packages")

    elif os.name == 'nt':
        #WINDOWS
        if system == "1":
            for lib in pip_install_linux:
                os.system(f"pip install {lib}")
        if system == "2":
            for lib in pip_install_remote:
                os.system(f"pip install {lib}")

    print("Installation Completed")
except KeyboardInterrupt:
    print("Installation Aborted")



