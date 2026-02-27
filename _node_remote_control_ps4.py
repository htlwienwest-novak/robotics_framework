# TelemetryBroker for Inter Process Communication for Robtics
# node for remote ps4 controler 
# Developed by Martin Novak at 2025/26
# 
from libs.lib_telemtrybroker import TelemetryBroker
import pygame
import sys

mb = TelemetryBroker()

data_dict = {"vel_linear_x":0, "vel_linear_y":0, "vel_angular_z":0, "tool_pen":0, "led_blink":0}

# Initialisierung
pygame.init()
pygame.joystick.init()


try:
    while True:
        # Überprüfen, ob Controller vorhanden sind
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            print("Kein Controller gefunden.")
            sys.exit()
        else:
            # Den ersten Controller auswählen (Index 0)
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            print(f"Controller erkannt: {joystick.get_name()}")
            print(f"Anzahl Achsen: {joystick.get_numaxes()}")
            print(f"Anzahl Buttons: {joystick.get_numbuttons()}")
            break

    print("-" * 20)
    print("Drücke Tasten auf dem Controller (STRG+C zum Beenden)...")

    # Hauptschleife

    while True:
        # Event-Handling
        for event in pygame.event.get():
            
            # Button gedrückt
            if event.type == pygame.JOYBUTTONDOWN:
                #print(f"Button gedrückt: ID {event.button}")
                if event.button == 0:   # X-Button
                    print("X-Button gedrückt")
                    if data_dict["tool_pen"] == 0:
                        data_dict["tool_pen"] = 1
                    else:
                        data_dict["tool_pen"] = 0

                elif event.button == 1: # Circle-Button
                    print("Circle-Button gedrückt")      
                    data_dict["led_blink"] = 1
                elif event.button == 3: # Square-Button
                    print("Square-Button gedrückt")
                elif event.button == 2: # Triangle-Button
                    print("Triangle-Button gedrückt")
                elif event.button == 9: # Share-Button
                    print("Share-Button gedrückt")
                elif event.button == 10: # Start-Button
                    print("Start-Button gedrückt")
                elif event.button == 6: # Options-Button
                    print("Options-Button gedrückt")
                elif event.button == 7: # LeftStick-Button
                    print("LeftStick-Button gedrückt")
                elif event.button == 8: # RightStick-Button
                    print("RightStick-Button gedrückt")
                elif event.button == 4: # L1-Button
                    print("L1-Button gedrückt")
                elif event.button == 5: # R1-Button
                    print("R1-Button gedrückt")
                elif event.button == 11: # Cross-Top-Button
                    print("Cross-Top-Button gedrückt")
                elif event.button == 12: # Cross-Bottom-Button
                    print("Cross-Bottom-Button gedrückt")
                elif event.button == 13: # Cross-Left-Button
                    print("Cross-Left-Button gedrückt")
                elif event.button == 14: # Cross-Right-Button
                    print("Cross-Right-Button gedrückt")
            
            # Button losgelassen
            elif event.type == pygame.JOYBUTTONUP:
                pass
            
            # Analoge Achsen (Sticks & Trigger L2/R2)
            elif event.type == pygame.JOYAXISMOTION:
                # Wir filtern sehr kleine Bewegungen (Deadzone), um Spam zu vermeiden
                if abs(event.value) > 0.1: 
                    #print(f"Achse {event.axis} bewegt: {int((event.value*100+100)/2):.2f}")
                    if event.axis == 0:
                        val = int(event.value*10)*10
                        if (val<20 and val>0) or (val>-20 and val<0):
                            val=0
                        print("Left-Stick-X bewegt:", val)
                        data_dict["vel_angular_z"] = val
                    elif event.axis == 1:
                        print("Left-Stick-Y bewegt:", int(event.value*100))
                    elif event.axis == 3:
                        val = int(event.value*10)*10
                        if (val<20 and val>0) or (val>-20 and val<0):
                            val=0
                        print("Right-Stick-X bewegt:", val)
                        data_dict["vel_linear_y"] = val                        
                    elif event.axis == 4:
                        val = int(event.value*10)*10*-1
                        if (val<20 and val>0) or (val>-20 and val<0):
                            val=0
                        print("Right-Stick-Y bewegt:", val)
                        data_dict["vel_linear_x"] = val   
                    elif event.axis == 2:
                        val = -1*int((event.value*100+100)/2)
                        print("L2-Trigger bewegt:", val)
                        #data_dict["vel_linear_x"] = val
                    elif event.axis == 5:
                        val = int((event.value*100+100)/2)
                        print("R2-Trigger bewegt:", val)
                        #data_dict["vel_linear_x"] = val
            
            # D-Pad (Steuerkreuz)
            elif event.type == pygame.JOYHATMOTION:
                # event.value ist ein Tuple, z.B. (0, 1) für Oben
                print(f"D-Pad (Hat {event.hat}) bewegt: {event.value}")
                
            # Quit Event (falls ein Fenster offen wäre)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mb.setmulti(data_dict)

        # Kurze Pause, um CPU-Last zu verringern (Clock tick wäre in einem Spiel besser)
        pygame.time.wait(10)

except KeyboardInterrupt:
    print("\nProgramm beendet.")
    pygame.quit()