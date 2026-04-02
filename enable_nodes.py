# TelemetryBroker for Inter Process Communication for Robtics
# Node as Remote Control via Console
# Developed by Martin Novak at 2025/26
from libs.lib_telemtrybroker import TelemetryBroker
import time
import os
from pathlib import Path

mb = TelemetryBroker()

num = 0
file_list = []
fileobj_list = []

# Verzeichnis festlegen ( . steht für den aktuellen Ordner )
pfad = Path('.')



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
        key_list = []
        data_dict = {}  
        
        for name in file_list:
            print(f"{num:>2} : {name}")
            num += 1

        print()

        # INPUT
        print("ENTER => refresh nodelist")
        print("s => start enabled nodes")
        print("x => stop all running nodes")
        print("q => quit")
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
        elif input_key == "s":
            print("Starting Nodes...")
            os.system("python starter.py")
        elif input_key == "q":
            break
        elif input_key == "x":
            print("Stopping Nodes...")
            os.system("python stop.py")
    except KeyboardInterrupt:
        break

mb.close()