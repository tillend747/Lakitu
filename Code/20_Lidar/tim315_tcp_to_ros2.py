#!/usr/bin/env python3
import socket
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

HOST = "192.168.10.32"  # IP des TiM-315
PORT = 2112
SCAN_TOPIC = "scan"
FRAME_ID = "laser"
RATE_HZ = 5  # Update-Rate

class Tim315TcpNode(Node):
    def __init__(self):
        super().__init__('tim315_tcp_node')
        self.publisher_ = self.create_publisher(LaserScan, SCAN_TOPIC, 10)
        self.timer = self.create_timer(1.0 / RATE_HZ, self.timer_callback)

        # TCP-Verbindung
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        try:
            self.sock.connect((HOST, PORT))
            self.get_logger().info(f"Verbunden mit TiM-315: {HOST}:{PORT}")
        except Exception as e:
            self.get_logger().error(f"Fehler beim Verbinden: {e}")
            rclpy.shutdown()

    def read_scan(self):
        """Sendet den TiM-Befehl und liest Scan-Daten zurück (ASCII)"""
        try:
            self.sock.sendall(b'\x02sRN LMDscandata\x03')
            data = self.sock.recv(8192)
            text = data.decode('ascii', errors='ignore')
            numbers = [int(x, 16) for x in text.split() if all(c in "0123456789ABCDEFabcdef" for c in x)]
            return numbers
        except Exception as e:
            self.get_logger().warn(f"Fehler beim Lesen: {e}")
            return []

    def create_laserscan(self, ranges):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = FRAME_ID
        msg.angle_min = -math.pi / 2
        msg.angle_max = math.pi / 2
        msg.angle_increment = (msg.angle_max - msg.angle_min) / max(len(ranges), 1)
        msg.time_increment = 0.0
        msg.scan_time = 1.0 / RATE_HZ
        msg.range_min = 0.05
        msg.range_max = 20.0
        msg.ranges = [r / 1000.0 for r in ranges]  # mm → m
        return msg

    def timer_callback(self):
        scan_data = self.read_scan()
        if scan_data:
            msg = self.create_laserscan(scan_data)
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Tim315TcpNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.sock.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
