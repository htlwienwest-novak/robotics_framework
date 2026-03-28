import cv2
import numpy as np
import time
from libs.lib_telemtrybroker import TelemetryBroker


TEMPLATE_PATH = "/home/robot/robotics_framework/libs/"


mb = TelemetryBroker() 
sensor_dict_orig = {"sensor_camera_color":"", "sensor_camera_letter":""}

# 1. Templates laden (in Graustufen)
# Stelle sicher, dass diese Bilder im gleichen Ordner liegen
templates = {
    "H": cv2.imread(TEMPLATE_PATH+'tpl_h.png', 0),
    "S": cv2.imread(TEMPLATE_PATH+'tpl_s.png', 0),
    "U": cv2.imread(TEMPLATE_PATH+'tpl_u.png', 0)
}

# Überprüfen, ob Templates geladen wurden
for key, tpl in templates.items():
    if tpl is None:
        raise Exception(f"Fehler: Template für {key} nicht gefunden!")

# Webcam oder Bildquelle initialisieren
cap = cv2.VideoCapture(0) 

# Schwellenwert für Übereinstimmung (0.8 = 80% Übereinstimmung)
# Spiel hiermit herum: Höher = genauer, aber übersieht evtl. was
THRESHOLD = 0.7

# Grün (ca. 40-80)
lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])

# Gelb (ca. 20-35)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([35, 255, 255])

# Rot ist speziell: Es liegt am Anfang (0-10) UND am Ende (170-180) des Spektrums
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

def scan_for_letters(frame):
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
            sensor_dict["sensor_camera_letter"] = char_name
            print("Victim Letter recognized:", char_name)
            # pt ist die Koordinate der oberen linken Ecke
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            
            # Buchstaben darüber schreiben
            cv2.putText(frame, char_name, (pt[0], pt[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

def scan_for_colors(frame):
    # COLOR DETECTION
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv_frame = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        
    mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    color_masks = {
        "green": (mask_green, (0, 255, 0)),  # Name, Maske, Anzeigefarbe (BGR)
        "yellow": (mask_yellow, (0, 255, 255)),
        "red": (mask_red, (0, 0, 255))
    }

    for color_name, (mask, display_color) in color_masks.items():
        # Rauschen entfernen (kleine weiße Punkte wegmachen)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            #for contour in contours:
            if cv2.contourArea(contours[0]) > 5000:
                x, y, w, h = cv2.boundingRect(contours[0])
                cv2.rectangle(frame, (x, y), (x + w, y + h), display_color, 2)
                cv2.putText(frame, color_name, (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, display_color, 2)
                print("Victim Color recognized:", color_name)
                sensor_dict["sensor_camera_color"] = color_name

    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    sensor_dict = sensor_dict_orig.copy()
    frame = scan_for_letters(frame)
    frame = scan_for_colors(frame)
    mb.setmulti(sensor_dict)
    #cv2.imshow('wall scanner', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()