# TelemetryBroker for Inter Process Communication for Robtics
# node for camera recognition
# Developed by Martin Novak at 2025/26
# pip install easyocr
# pip uninstall opencv-python opencv-python-headless
# pip install opencv-python

import cv2
import easyocr
import numpy as np

from libs.lib_telemtrybroker import TelemetryBroker

mb = TelemetryBroker() 

sensor_dict_orig = {"sensor_camera_color":"", "sensor_camera_letter":""}


# Reader initialisieren
# 'de' für Deutsch, 'en' für Englisch. gpu=False, falls du keine Nvidia-Karte hast.
reader = easyocr.Reader(['en'], gpu=False) 

cap = cv2.VideoCapture(0)

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

while True:
    try:
        sensor_dict = sensor_dict_orig.copy()

        ret, frame = cap.read()
        if not ret:
            break

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

        
        # EASYOCR: LETTER DETECTION
        # detail=0 gibt nur den Text zurück, ohne Koordinaten
        results = reader.readtext(frame)

        for (bbox, text, prob) in results:
            if prob > 0.7:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = (int(top_left[0]), int(top_left[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, text, (top_left[0], top_left[1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                print(f"Erkannt: {text} (Sicherheit: {prob:.2f})")
                if text.lower()=="h" or text.lower()=="s" or text.lower()=="u":
                    print("Victim Letter recognized:", text.lower())
                    sensor_dict["sensor_camera_letter"] = text.lower()

        mb.setmulti(sensor_dict)

        #cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    except Exception as e:
        print(e)
        break

mb.close()
cap.release()
cv2.destroyAllWindows()