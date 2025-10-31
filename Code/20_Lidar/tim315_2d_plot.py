import socket
import struct
import numpy as np
import matplotlib.pyplot as plt

# IP und Port des TIM315
HOST = "192.168.10.32"
PORT = 2112  # Standard Port

# TCP-Verbindung öffnen
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Matplotlib-Setup
plt.ion()
fig, ax = plt.subplots()
sc = ax.scatter([], [], s=2)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")

def parse_lidar_data(data_bytes):
    """
    Beispiel: Parse TIM315 Lidar Daten in XY-Koordinaten.
    Hier musst du ggf. das Datenformat deines Lidar anpassen.
    """
    # Dummy parsing
