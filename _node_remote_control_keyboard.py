# TelemetryBroker for Inter Process Communication for Robtics
# node for remote by keyboard
# Developed by Martin Novak at 2025/26
# 
from libs.lib_telemtrybroker import TelemetryBroker
from pynput import keyboard
import os

mb = TelemetryBroker()

data_dict = {"vel_linear_x":0, "vel_linear_y":0, "vel_angular_z":0, "tool_pen":0, "led_blink":0}

speed = 100

def on_press(key):
    global speed
    try:
        if key == keyboard.Key.up:
            speed += 10
            if speed > 100:
                speed = 100
        elif key == keyboard.Key.down:
            speed -= 10
            if speed < 0:
                speed = 0   


        if key.char == 'w':
            data_dict["vel_linear_x"] = speed
        elif key.char == 's':
            data_dict["vel_linear_x"] = -speed
        elif key.char == 'a':
            data_dict["vel_angular_z"] = -speed
        elif key.char == 'd':
            data_dict["vel_angular_z"] = speed
        elif key.char == 'q':
            data_dict["vel_linear_y"] = -speed
        elif key.char == 'e':
            data_dict["vel_linear_y"] = speed
        elif key.char == 'p':
            if data_dict["tool_pen"] == 0:
                data_dict["tool_pen"] = 1
            else:
                data_dict["tool_pen"] = 0
        elif key.char == 'l':
            if data_dict["led_blink"] == 0:
                data_dict["led_blink"] = 1
            else:
                data_dict["led_blink"] = 0
        

        mb.setmulti(data_dict)

    except AttributeError:
        pass

def on_release(key):
    data_dict["vel_linear_x"] = 0
    data_dict["vel_linear_y"] = 0
    data_dict["vel_angular_z"] = 0
    mb.setmulti(data_dict)
    if key == keyboard.Key.esc:
        return False # Beendet das Programm
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"SPEED: {speed}")
    print()
    print(f"W => forward")
    print(f"S => backward")
    print(f"A => turn left")
    print(f"D => turn right")
    print(f"Q => strafe left")
    print(f"E => strafe right")
    print(f"P => toggle tool pen")
    print(f"L => toggle led blink")
    print(f"UP => increase speed")
    print(f"DOWN => decrease speed")
    print(f"ESC => exit")


os.system('cls' if os.name == 'nt' else 'clear')
print(f"SPEED: {speed}")
print()
print(f"W => forward")
print(f"S => backward")
print(f"A => turn left")
print(f"D => turn right")
print(f"Q => strafe left")
print(f"E => strafe right")
print(f"P => toggle tool pen")
print(f"L => toggle led blink")
print(f"UP => increase speed")
print(f"DOWN => decrease speed")
print(f"ESC => exit")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
