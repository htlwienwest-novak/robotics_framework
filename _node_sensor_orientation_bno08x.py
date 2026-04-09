# TelemetryBroker for Inter Process Communication for Robtics
# node for BNO08x orientation and psoition sensor
# sensor system with 3 sensors: Accelerometer, Gyroscope, Magnetometer
# Developed by Martin Novak at 2025/26
# Installation on raspberry pi:
#   pip install adafruit-blinka
#   pip install adafruit-circuitpython-bno08x


from libs.lib_telemtrybroker import TelemetryBroker
import time
import board
import math
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import (BNO_REPORT_ROTATION_VECTOR, BNO_REPORT_LINEAR_ACCELERATION)

# I2C Initialisierung (Adresse 0x4b)
i2c = board.I2C()
bno = BNO08X_I2C(i2c, address=0x4b)

# Rotation Vector aktivieren (Fusion aus Accel, Gyro, Mag)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)

mb = TelemetryBroker()

data_dict = {"sensor_angular_abs_z":0, "sensor_angular_abs_y":0, "sensor_angular_abs_x":0, 
               "sensor_linear_rel_x":0, "sensor_linear_rel_y":0, "sensor_linear_rel_z":0,
               "sensor_angular_abs_z_offset":0}

mb.setmulti(data_dict)

def quaternion_to_euler(quat):
    """
    Konvertiert Quaternions (x, y, z, w) in Euler-Winkel (Roll, Pitch, Yaw)
    """
    x, y, z, w = quat

    # Roll (X-Achse)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # Pitch (Y-Achse)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp) # 90 Grad bei Limit
    else:
        pitch = math.asin(sinp)

    # Yaw (Z-Achse / Heading)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    # Umrechnung in Grad
    roll_deg = math.degrees(roll)
    pitch_deg = math.degrees(pitch)
    yaw_deg = math.degrees(yaw)

    # Yaw auf 0-360 Grad normieren
    if yaw_deg < 0:
        yaw_deg += 360

    return roll_deg, pitch_deg, yaw_deg

print("BNO08x 3-Achsen-Messung aktiv...")


try:
    while True:
        quat = bno.quaternion
        
        if quat is not None:
            r, p, y = quaternion_to_euler(quat)
            lin_x, lin_y, lin_z = bno.linear_acceleration
            #print(f"LINEAR -> X: {lin_x:6.2f} Y: {lin_y:6.2f} Z: {lin_z:6.2f}")
            #print(f"X (Roll): {r:7.2f}° | Y (Pitch): {p:7.2f}° | Z (Yaw): {y:7.2f}°")

            data_dict["sensor_angular_abs_x"] = int(r)
            data_dict["sensor_angular_abs_y"] = int(p)
            data_dict["sensor_angular_abs_z"] = int(y) - mb.get("sensor_angular_abs_z_offset")  # Offset für Yaw (Heading) berücksichtigen
            data_dict["sensor_linear_rel_x"] = round(lin_x,2)
            data_dict["sensor_linear_rel_y"] = round(lin_y,2)
            data_dict["sensor_linear_rel_z"] = round(lin_z,2)

            mb.setmulti(data_dict)
        time.sleep(0.05) # 20Hz Update-Rate

except KeyboardInterrupt:
    print("\nMessung beendet.")
    mb.close()