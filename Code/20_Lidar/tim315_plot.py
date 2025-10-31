#!/usr/bin/env python3
import socket
import struct
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import time

# ------------------------
# Konfiguration
# ------------------------
LIDAR_IP = "192.168.10.32"
LIDAR_PORT = 2112
USE_3D = False  # True = Open3D 3D Plot, False = Matplotlib 2D

# ------------------------
# TCP Verbindung aufbauen
# ------------------------
def connect_lidar(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    s.connect((ip, port))
    print(f"Verbunden mit Lidar {ip}:{port}")
    return s

# ------------------------
# Dummy-Funktion: Lidar-Daten lesen
# ------------------------
def read_points(sock):
    """
    Ersetze dies mit dem richtigen TCP-Protokoll
    des TIM315. Hier simuliert es zufällige Punkte.
    """
    # Beispiel: 100 zufällige Punkte in 2D oder 3D
    if USE_3D:
        points = np.random.uniform(-5, 5, (100, 3))
    else:
        points = np.random.uniform(-5, 5, (100, 2))
    return points

# ------------------------
# Visualisierung starten
# ------------------------
if USE_3D:
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.geometry.PointCloud()
else:
    plt.ion()
    fig, ax = plt.subplots()

# ------------------------
# Hauptloop
# ------------------------
try:
    sock = connect_lidar(LIDAR_IP, LIDAR_PORT)
    while True:
        points = read_points(sock)

        if USE_3D:
            pcd.points = o3d.utility.Vector3dVector(points)
            vis.add_geometry(pcd)
            vis.update_geometry(pcd)
            vis.poll_events()
            vis.update_renderer()
        else:
            ax.clear()
            xs, ys = zip(*points)
            ax.scatter(xs, ys)
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel("X [m]")
            ax.set_ylabel("Y [m]")
            plt.draw()
            plt.pause(0.1)

except KeyboardInterrupt:
    print("Beende...")
    if USE_3D:
        vis.destroy_window()
    sock.close()
