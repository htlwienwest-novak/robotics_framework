# TelemetryBroker for Inter Process Communication for Robtics
# KILL all running Nodes
# Developed by Martin Novak at 2025/26
# pip install psutil

import psutil
import os


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

    if gefundene_prozesse == 0:
        print("[i] Keine passenden Skripte gefunden.")
    else:
        print(f"[!] Insgesamt {gefundene_prozesse} Skripte gestoppt.")

if __name__ == "__main__":
    auto_kill_node_scripts()