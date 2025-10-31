import socket
import struct
import numpy as np
import open3d as o3d

# TCP-Verbindung zum Lidar
HOST = '192.168.10.32'  # IP des TIM315
PORT = 2112              # Standard TCP-Port

def parse_points(data):
    """
    Dummy-Parser für Lidar-Daten.
    Hier musst du ggf. das TIM315-Datenformat anpassen.
    """
    # Beispiel: jede Messung 3 floats (x,y,z)
    # Bei echtem TIM315: parse das SOPAS-Protokoll
    points = []
    for i in range(0, len(data), 12):
        x, y, z = struct.unpack('fff', data[i:i+12])
        points.append([x, y, z])
    return np.array(points)

def main():
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='TIM315 Live Pointcloud')
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Verbunden mit TIM315")

        while True:
            try:
                data = s.recv(12000)  # empfange Block mit Punkten
                if not data:
                    continue

                points = parse_points(data)
                pcd.points = o3d.utility.Vector3dVector(points)
                vis.update_geometry(pcd)
                vis.poll_events()
                vis.update_renderer()
            except KeyboardInterrupt:
                print("Beendet durch Benutzer")
                break

    vis.destroy_window()

if __name__ == '__main__':
    main()
