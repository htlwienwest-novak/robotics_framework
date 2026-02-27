import cv2
import numpy as np
import time

# 1. Templates laden (in Graustufen)
# Stelle sicher, dass diese Bilder im gleichen Ordner liegen
templates = {
    "H": cv2.imread('tpl_h.png', 0),
    "S": cv2.imread('tpl_s.png', 0),
    "U": cv2.imread('tpl_u.png', 0)
}

# Überprüfen, ob Templates geladen wurden
for key, tpl in templates.items():
    if tpl is None:
        raise Exception(f"Fehler: Template für {key} nicht gefunden!")

# Webcam oder Bildquelle initialisieren
cap = cv2.VideoCapture(0) 

# Schwellenwert für Übereinstimmung (0.8 = 80% Übereinstimmung)
# Spiel hiermit herum: Höher = genauer, aber übersieht evtl. was
THRESHOLD = 0.8

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Performance: Bild in Graustufen umwandeln
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Durch alle Templates loopen (H, S, U)
    for char_name, template in templates.items():
        w, h = template.shape[::-1]

        # Das eigentliche Matching
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        
        # Finde alle Positionen, die gut genug passen (über Threshold)
        loc = np.where(res >= THRESHOLD)

        # Rechtecke zeichnen
        for pt in zip(*loc[::-1]):
            # pt ist die Koordinate der oberen linken Ecke
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            
            # Buchstaben darüber schreiben
            cv2.putText(frame, char_name, (pt[0], pt[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Buchstaben Erkennung', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()