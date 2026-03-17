# TelemetryBroker for Inter Process Communication for Robtics
# ExampleNode: Client for Transmitter Nodes
# Developed by Martin Novak at 2025/26
import random
from libs.lib_telemtrybroker import TelemetryBroker
from flask import Flask, request, jsonify

mb = TelemetryBroker() 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_json():
    if request.method == 'POST':
        # Prüfen, ob die Daten im JSON-Format vorliegen
        if request.is_json:
            # Den JSON-String automatisch in ein Python-Dictionary umwandeln
            data = request.get_json()
            print(f"Empfangene Daten: {data}")

            for key, value in data.items():
                mb.set(key, value)  # Setze die Werte im TelemetryBroker

            # Eine Antwort zurückgeben
            return "ok", 200
        else:
            return jsonify({"fehler": "Anfrage muss JSON sein"}), 400
    elif request.method == 'GET':
        data = request.args.to_dict()
        for key, value in data.items():
            mb.set(key, value)  # Setze die Werte im TelemetryBroker
        return "ok", 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

mb.close()
