# TelemetryBroker for Inter Process Communication for Robtics
# Visualitation for Slamtec RPLidar C1 distance sensors
# sensor system with 4 sensors: front, right, left, back
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
# pip install matplotlib, numpy

from libs.lib_telemtrybroker import TelemetryBroker
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

mb = TelemetryBroker()

mb.set("sensor_distance_360", {0:100, 90:100, 180:100, 270:100})


# Falls deine Winkel in Grad sind, müssen wir sie für Matplotlib in Bogenmaß (Radians) umrechnen
def get_lidar_data():
    res = mb.get("sensor_distance_360")
    return {int(k): v for k, v in res.items()}


# Initialisierung des Plots
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

line, = ax.plot([], [], 'ro', markersize=2)  # 'ro' für rote Punkte

# Plot-Einstellungen
ax.set_ylim(0, 200)  # Maximale Reichweite deines Sensors (z.B. 5 Meter)
ax.set_title("Echtzeit LiDAR Scan", va='bottom')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    # Hier liest du dein Dictionary ein
    data = get_lidar_data()
    
    # Daten im Plot aktualisieren
    angles_rad = np.radians(list(data.keys()))
    distances = list(data.values())
    line.set_data(angles_rad, distances)
    return line,

# Animation starten
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=1)

plt.show()


        
