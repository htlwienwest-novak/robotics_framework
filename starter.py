# TelemetryBroker for Inter Process Communication for Robtics
# Starter for all Nodes
# Developed by Martin Novak at 2025/26
#   - Nodes must be in the same folder of starter.py
#   - Filename must be start with "node_", example "node_sensor.py"
#   - Deactivate autostart for a file, rename it, example "_node_sensor.py"
# Autostart script installation:
#   1 - sudo nano ~/.config/autostart/nodestarter.desktop
#   2 - Insert following lines:
#       [Desktop Entry]
#       Type=Application
#       Name=Node Starter
#       Exec=python3 /home/pi/desktop/starter.py
#       Terminal=true
import os
import subprocess
import glob
import time

#time.sleep(5)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
MUSTER = "node_*.py"

files = glob.glob(os.path.join(SCRIPT_PATH, MUSTER))

print("Start of", len(files), "nodes from path:", SCRIPT_PATH)

for file in files:
    print(file)
    #LINUX:
    #command = f'python "{file}"; echo "Skript beendet. Drücke Enter zum Schließen..."; read'
    #subprocess.Popen(["lxterminal", "--command", f"bash -c '{command}'"])

    #WINDOWS:
    command = f'python "{file}"'
    subprocess.Popen(f'start cmd /k "{command}"', shell=True)