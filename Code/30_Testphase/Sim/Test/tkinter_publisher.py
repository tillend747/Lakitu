import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tkinter as tk
from tkinter import Scale, Label
import threading
import time

# --- ROS 2 Node Klasse ---
class CmdVelPublisher(Node):
    """Ein ROS 2 Node, das Twist-Nachrichten an das Fahrzeug sendet."""
    
    # Topic-Name des Controllers aus der SDF/YAML-Konfiguration
    TOPIC_NAME = '/vehicle_blue_diff_drive_controller/cmd_vel'

    def __init__(self):
        super().__init__('cmd_vel_publisher_node')
        # Erstellt den Publisher für das Topic mit dem Typ Twist
        self.publisher_ = self.create_publisher(Twist, self.TOPIC_NAME, 10)
        self.get_logger().info(f'ROS 2 Publisher initialisiert. Topic: {self.TOPIC_NAME}')

    def publish_twist(self, linear_x, angular_z):
        """Erstellt und sendet eine Twist-Nachricht."""
        
        msg = Twist()
        # Lineare Geschwindigkeit auf der x-Achse (vorwärts/rückwärts)
        msg.linear.x = float(linear_x)
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        
        # Winkelgeschwindigkeit um die z-Achse (Drehung)
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = float(angular_z)
        
        self.publisher_.publish(msg)
        # self.get_logger().info(f'Sende: Linear X={linear_x:.2f}, Angular Z={angular_z:.2f}')
        
# --- Tkinter GUI Klasse ---
class VelocityController(tk.Frame):
    """Die Tkinter-GUI-Anwendung mit Slidern zur Geschwindigkeitssteuerung."""

    def __init__(self, master=None, ros_node=None):
        super().__init__(master)
        self.master = master
        self.ros_node = ros_node
        self.master.title("ROS 2 Velocity Controller")
        self.pack(padx=20, pady=20)
        
        # Timer für kontinuierliches Publizieren
        self.master.after(100, self.timer_callback) # Publiziert alle 100 ms (10 Hz)
        
        self.create_widgets()

    def create_widgets(self):
        
        # --- Lineare Geschwindigkeit (Linear X) ---
        Label(self, text="Lineare Geschwindigkeit X (m/s)").pack(pady=(15, 5))
        self.linear_scale = Scale(
            self, 
            from_=-2.0, to=2.0,          # Von -2.0 m/s (Rückwärts) bis 2.0 m/s (Vorwärts)
            resolution=0.1,              # Auflösung des Schiebereglers
            orient=tk.HORIZONTAL,
            length=300
        )
        self.linear_scale.set(0.0) # Startwert
        self.linear_scale.pack()

        # --- Winkelgeschwindigkeit (Angular Z) ---
        Label(self, text="Winkelgeschwindigkeit Z (rad/s)").pack(pady=(15, 5))
        self.angular_scale = Scale(
            self, 
            from_=-1.5, to=1.5,          # Von -1.5 rad/s (rechts) bis 1.5 rad/s (links)
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.angular_scale.set(0.0) # Startwert
        self.angular_scale.pack()

        # --- Stopp-Button ---
        self.stop_button = tk.Button(self, text="STOP (0, 0)", fg="red",
                                     command=self.stop_robot)
        self.stop_button.pack(pady=20, fill=tk.X)

    def stop_robot(self):
        """Setzt beide Geschwindigkeiten auf Null und sendet den Befehl."""
        self.linear_scale.set(0.0)
        self.angular_scale.set(0.0)
        self.send_command()

    def send_command(self):
        """Liest die aktuellen Slider-Werte und publiziert sie über ROS 2."""
        linear_x = self.linear_scale.get()
        angular_z = self.angular_scale.get()
        
        if self.ros_node:
            self.ros_node.publish_twist(linear_x, angular_z)
        else:
            print("ROS 2 Node nicht verfügbar.")

    def timer_callback(self):
        """Wird regelmässig aufgerufen, um die aktuellen Werte zu senden."""
        self.send_command()
        # Plant den nächsten Aufruf (Publizierrate von 10 Hz)
        self.master.after(100, self.timer_callback)
        
# --- Haupt-Funktion und Threading (wie zuvor) ---

def ros_spin_thread(node):
    """Führt rclpy.spin() in einem separaten Thread aus."""
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    publisher_node = CmdVelPublisher()

    # ROS 2 Spin in einem separaten Thread starten (ESSENTIELL)
    ros_thread = threading.Thread(target=ros_spin_thread, args=(publisher_node,))
    ros_thread.start()

    # Tkinter GUI erstellen und starten
    root = tk.Tk()
    app = VelocityController(master=root, ros_node=publisher_node)
    app.mainloop()

    # Aufräumen
    print("GUI geschlossen. Warte auf ROS-Thread-Ende...")
    ros_thread.join()
    print("ROS 2 Velocity Controller beendet.")

if __name__ == '__main__':
    main()