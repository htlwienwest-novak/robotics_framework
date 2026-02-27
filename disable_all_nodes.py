# rename all node files to _node

from pathlib import Path

# Verzeichnis festlegen ( . steht für den aktuellen Ordner )
pfad = Path('.')

# Suche nach allen Dateien, die mit 'node_' beginnen
for datei in pfad.glob('node_*'):
    # Prüfen, ob es wirklich eine Datei ist (kein Ordner)
    if datei.is_file():
        # Neuen Namen erstellen: _ + alter Name
        neuer_name = f"_{datei.name}"
        
        # Umbenennen
        try:
            datei.rename(pfad / neuer_name)
            print(f"Erfolg: {datei.name} -> {neuer_name}")
        except Exception as e:
            print(f"Fehler bei {datei.name}: {e}")

if not list(pfad.glob('node_*')):
    print("Keine Dateien mit dem Muster 'node_*' gefunden.")