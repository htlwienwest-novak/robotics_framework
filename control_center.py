# TelemetryBroker for Inter Process Communication for Robtics
# Node as Remote Control via Console
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os
from pathlib import Path
import psutil
from rich.live import Live
from rich.table import Table
import subprocess
import glob

mb = TelemetryBroker()

num = 0
file_list = []
fileobj_list = []

# Verzeichnis festlegen ( . steht für den aktuellen Ordner )
pfad = Path('.')

ROT = "\033[31m"
GRUEN = "\033[32m"
GELB = "\033[33m"
BLAU = "\033[34m"
RESET = "\033[0m" # Ganz wichtig, um die Farbe wieder zurückzusetzen!


def menu_node_management():
    while True:
        try:
            file_list = []
            fileobj_list = []

            for datei in pfad.glob('*node_*'):
                # Prüfen, ob es wirklich eine Datei ist (kein Ordner)
                if datei.is_file():
                    # Neuen Namen erstellen: _ + alter Name
                    file_list.append(datei.name)
                    fileobj_list.append(datei)


            os.system('cls' if os.name == 'nt' else 'clear')
            num = 0
            
            print(f"{GELB}CONTROL CENTER - NODE MANAGEMENT{RESET}")

            for name in file_list:
                if name.startswith("_"):
                    print(f"{ROT}{num:>2} : {name}{RESET}")
                else:
                    print(f"{GRUEN}{num:>2} : {name}{RESET}")
                num += 1

            print()

            # INPUT
            print(f"{GELB}ENTER => refresh nodelist")
            print(f"{ROT}b => back to HOME{RESET}")
            input_key = input("enable/disable node with number: ")

            if input_key == "":
                continue

            if input_key.isdigit():
                file_name = file_list[int(input_key)]

                if file_name.startswith("_"):
                    file_name = file_name[1:]
                else:
                    file_name = f"_{file_name}"
                    
                # Umbenennen
                try:
                    datei = fileobj_list[int(input_key)]
                    datei.rename(pfad / file_name)
                    #print(f"Erfolg: {datei.name} -> {file_name}")
                except Exception as e:
                    print(f"Fehler bei {datei.name}: {e}")
            elif input_key == "b":
                break
        except KeyboardInterrupt:
            break

def start_installer():
    pip_install_start = [
        "redis",
        "psutil",
        "rich"
    ]

    for lib in pip_install_start:
        if os.name == 'posix':
            os.system(f"pip install {lib} --break-system-packages")
        elif os.name == 'nt':
            os.system(f"pip install {lib}")
        else:
            print("Unknown OS")


def menu_installer():
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
        "pynput"
    ]

    pip_install_remote = [
        "redis",
        "matplotlib",
        "numpy",
        "rich",
        "pynput"
    ]

    pip_install_sim = [
        "redis",
        "rich",
        "openpyxl",
        "scipy",
        "shapely",
        "pygame",
        "pynput"
    ]


    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{GELB}LIBRARY INSTALLER FOR ROBOTICS FRAMEWORK{RESET}")
        print()
        if os.name == 'posix':
            print("Linux OS detected!")
        elif os.name == 'nt':
            print("Windows OS detected!")
        else:
            print("Unknown OS")
            exit()
        print()
        print("Which Libraries do you want to install?")
        print("1 => Fully Robot")
        print("2 => Remote only")
        print("3 => Simulation only")
        print()
        print(f"{ROT}b => back to HOME{RESET}")
        system = input("Enter your choice: ")
        
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
        if system == "b":
            pass
        
        print("Installation Completed")
    except KeyboardInterrupt:
        print("Installation Aborted")


def auto_kill_node_scripts():
    # Wir holen uns die eigene PID, damit das Skript sich nicht selbst beendet
    meine_pid = os.getpid()
    gefundene_prozesse = 0

    print("Suche nach laufenden Python-Skripten, die mit 'node' beginnen...")

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline_liste = proc.info.get('cmdline')
            
            # Falls der Prozess keine Commandline hat (z.B. System-Kern), überspringen
            if not cmdline_liste or len(cmdline_liste) < 2:
                continue

            # Wir prüfen: 
            # 1. Ist es ein Python-Prozess?
            # 2. Enthält das erste Argument (das Skript) das Wort 'node' am Anfang?
            befehl = " ".join(cmdline_liste)
            script_pfad = cmdline_liste[1]
            script_name = os.path.basename(script_pfad)

            if "python" in proc.info['name'].lower() and script_name.startswith("node"):
                if proc.info['pid'] != meine_pid:
                    print(f"[*] Beende automatisch: {script_name} (PID: {proc.info['pid']})")
                    parent = proc.parent()
                    proc.terminate()
                    if parent:
                        parent.kill()
                    #proc.kill()
                    gefundene_prozesse += 1


        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    mb.clearall()

    if gefundene_prozesse == 0:
        print("[i] Keine passenden Skripte gefunden.")
    else:
        print(f"[!] Insgesamt {gefundene_prozesse} Skripte gestoppt.")


def menu_command_center():
    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
    MUSTER = "*node_remote_control_terminal.py"

    files = glob.glob(os.path.join(SCRIPT_PATH, MUSTER))

    for file in files:
        print(file)

        if os.name == 'posix':
            #LINUX:
            command = f'python "{file}"; echo "Skript beendet. Drücke Enter zum Schließen..."; read'
            subprocess.Popen(["lxterminal", "--command", f"bash -c '{command}'"])

        elif os.name == 'nt':
            #WINDOWS:
            command = f'python "{file}"'
            subprocess.Popen(f'start cmd /k "{command}"', shell=True)

def menu_show_live_data():
    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
    MUSTER = "*node_remote_display_terminal.py"

    files = glob.glob(os.path.join(SCRIPT_PATH, MUSTER))

    for file in files:
        print(file)

        if os.name == 'posix':
            #LINUX:
            command = f'python "{file}"; echo "Skript beendet. Drücke Enter zum Schließen..."; read'
            subprocess.Popen(["lxterminal", "--command", f"bash -c '{command}'"])

        elif os.name == 'nt':
            #WINDOWS:
            command = f'python "{file}"'
            subprocess.Popen(f'start cmd /k "{command}"', shell=True)


start_installer()
mb.clearall()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{GRUEN}CONTROL CENTER{RESET}")
    print()
    print(f"s => START All Enabled Nodes")
    print(f"x => STOP All Running Nodes")
    print()
    print(f"{GELB}1 => Node Management{RESET}")
    print(f"{GELB}2 => Manual Control via Console{RESET}")
    print(f"{GELB}3 => Show Live Data{RESET}")
    print(f"{GELB}4 => Installer for Libs and Drivers{RESET}")
    print()
    print(f"{ROT}q => Quit{RESET}")
    input_key = input("command: ")
    if input_key == "q":
        break
    elif input_key == "s":
        os.system("python starter.py")
    elif input_key == "1":
        menu_node_management()
    elif input_key == "2":
        menu_command_center()
    elif input_key == "3":
        menu_show_live_data()
    elif input_key == "4":
        menu_installer()
    elif input_key == "x":
        auto_kill_node_scripts()
    else:
        continue    
    
mb.close()