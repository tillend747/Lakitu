#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Point, Vector3
from tf2_ros import TransformBroadcaster # Import für TF-Broadcaster
from geometry_msgs.msg import TransformStamped # Import für TF-Nachricht
import numpy as np
import math

class ImuOdometryNode(Node):
    def __init__(self):
        super().__init__('imu_odometry_node')

        # 1. Zustandsspeicher (Initialisierung)
        self.position = np.array([0.0, 0.0, 0.0])  # [x, y, z] in Metern
        self.velocity = np.array([0.0, 0.0, 0.0])  # [vx, vy, vz] in m/s
        self.last_time = self.get_clock().now()
        
        # Speicher für die letzte IMU-Nachricht (wird für die Orientierung benötigt)
        self.last_imu_msg = None 

        # 2. Publisher und Subscriber definieren
        self.odom_pub = self.create_publisher(Odometry, 'odom_imu', 10)
        self.imu_sub = self.create_subscription(
            Imu, 
            'imu/data', 
            self.imu_callback, 
            10
        )
        
        # 3. TF Broadcaster initialisieren
        self.tf_broadcaster = TransformBroadcaster(self)

        # 4. TIMER zur langsameren Veröffentlichung hinzufügen (z.B. 30 Hz)
        # RViz kann dies besser verarbeiten
        PUBLISHING_FREQUENCY = 10.0 # Hz
        self.publish_timer = self.create_timer(1.0 / PUBLISHING_FREQUENCY, self.publish_odom_data)

        self.get_logger().info(
            f"IMU Odometry Node gestartet. Integration bei 100 Hz, Veröffentlichung bei {PUBLISHING_FREQUENCY} Hz."
        )

    def imu_callback(self, imu_msg):
        """Führt die Integration der Position und Geschwindigkeit mit hoher Frequenz durch."""
        
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        if dt <= 0.0:
            return

        # Speichere die aktuelle IMU-Nachricht für die Verwendung im Publishing-Timer
        self.last_imu_msg = imu_msg
        
        # Lineare Beschleunigung extrahieren
        ax = imu_msg.linear_acceleration.x
        ay = imu_msg.linear_acceleration.y
        az = imu_msg.linear_acceleration.z 
        
        acceleration = np.array([ax, ay, az])
        
        # Integration (Euler-Methode)   
        # Geschwindigkeit integrieren: v_neu = v_alt + a * dt
        self.velocity += acceleration * dt

        # Position integrieren: p_neu = p_alt + v_neu * dt
        self.position += self.velocity * dt


    def publish_odom_data(self):
        """Erstellt und veröffentlicht die Odometrie-Nachricht und das TF mit reduzierter Frequenz."""
        
        if self.last_imu_msg is None:
            return # Warten auf die erste IMU-Nachricht

        current_time = self.get_clock().now()
        
        # 1. Odometry-Nachricht erstellen und füllen
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'        # Frame des Weltkoordinatensystems
        odom.child_frame_id = 'imu_link'    # Frame des Sensors (Kinder-Frame)
        
        # Position füllen
        odom.pose.pose.position = Point(
            x=self.position[0], 
            y=self.position[1], 
            z=self.position[2]
        )
        
        # Orientierung füllen (direkt von der IMU)
        odom.pose.pose.orientation = self.last_imu_msg.orientation
        
        # Geschwindigkeit füllen
        odom.twist.twist.linear = Vector3(
            x=self.velocity[0], 
            y=self.velocity[1], 
            z=self.velocity[2]
        )
        # Winkelgeschwindigkeit (Gyro) kann direkt übernommen werden
        odom.twist.twist.angular = self.last_imu_msg.angular_velocity
        
        # 2. Odometrie veröffentlichen
        self.odom_pub.publish(odom)

        # 3. TF (Transform) senden
        self.publish_odom_transform(odom)


    def publish_odom_transform(self, odom_msg):
        """Sendet die Transformation von 'odom' nach 'imu_link'."""
        
        t = TransformStamped()

        # Header-Informationen
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = odom_msg.header.frame_id      # 'odom'
        t.child_frame_id = odom_msg.child_frame_id        # 'imu_link'

        # Position (Translation)
        t.transform.translation.x = odom_msg.pose.pose.position.x
        t.transform.translation.y = odom_msg.pose.pose.position.y
        t.transform.translation.z = odom_msg.pose.pose.position.z

        # Orientierung (Rotation)
        t.transform.rotation = odom_msg.pose.pose.orientation

        # Senden des Transforms
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = ImuOdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()