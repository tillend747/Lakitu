#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import serial
import time # Hinzugefügt für die Pufferbereinigung

class ImuSerialNode(Node):
    def __init__(self):
        super().__init__('imu_serial_bridge')

        # 1. Publisher definieren
        self.pub = self.create_publisher(Imu, 'imu/data', 10)

        # 2. Parameter deklarieren
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud', 115200)

        port = self.get_parameter('port').get_parameter_value().string_value
        baud = self.get_parameter('baud').get_parameter_value().integer_value

        # 3. Serielle Schnittstelle öffnen
        self.get_logger().info(f"Opening serial port: {port} @ {baud}")
        try:
            self.ser = serial.Serial(port, baud, timeout=0.05)
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port {port}: {e}")
            raise SystemExit

        # 4. Pufferbereinigung für robusten Start (ignoriert Initialisierungsdaten des IMU/Arduinos)
        self.get_logger().info("Waiting 1 second and flushing serial buffer...")
        time.sleep(1.0) 
        self.ser.reset_input_buffer()
        self.get_logger().info("Serial buffer flushed. Starting data read.")

        # 5. Timer für die Lese-Callback (100 Hz)
        self.timer = self.create_timer(0.01, self.timer_callback)

    def timer_callback(self):
        try:
            # Zeile lesen, dekodieren. Ungültige UTF-8-Zeichen werden ignoriert.
            line = self.ser.readline().decode('utf-8', errors='ignore').strip()
            
            if not line:
                return

            parts = line.split(',')
            # Erwartete Datenpunkte: t, qx, qy, qz, qw, ax, ay, az, gx, gy, gz (11 Werte)
            if len(parts) != 11:
                # Das passiert oft, wenn die Zeile unvollständig ist. 
                # Wir loggen dies nicht als Fehler, um die Konsole nicht zu überfluten.
                return

            # Konvertierung der String-Teile in float
            t, qx, qy, qz, qw, ax, ay, az, gx, gy, gz = map(float, parts)

            # 6. ROS 2 Imu Nachricht erstellen und füllen
            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "imu_link"

            # Orientierung (Quaternion)
            msg.orientation.x = qx
            msg.orientation.y = qy
            msg.orientation.z = qz
            msg.orientation.w = qw
            
            # WICHTIG: Die Kovarianzmatrizen werden nicht vom seriellen Gerät geliefert und bleiben daher 0 (unbestimmt).

            # Winkelgeschwindigkeit (Gyroscope)
            msg.angular_velocity.x = gx
            msg.angular_velocity.y = gy
            msg.angular_velocity.z = gz

            # Lineare Beschleunigung
            msg.linear_acceleration.x = ax
            msg.linear_acceleration.y = ay
            msg.linear_acceleration.z = az

            # 7. Nachricht veröffentlichen
            self.pub.publish(msg)

        except ValueError:
             # Tritt auf, wenn map(float, parts) fehlschlägt (z.B. bei nicht-numerischen Werten)
             self.get_logger().warn(f"Value error when parsing IMU data: {line}")
        except Exception as e:
            # Fang alle anderen unerwarteten Fehler ab (z.B. serielle Lesefehler)
            self.get_logger().error(f"An unexpected error occurred: {e}")


def main(args=None):
    rclpy.init(args=args)
    try:
        node = ImuSerialNode()
        rclpy.spin(node)
    except SystemExit:
        # Beendet sauber, wenn die serielle Schnittstelle nicht geöffnet werden konnte
        pass
    except KeyboardInterrupt:
        pass
    finally:
        if 'node' in locals() and node is not None:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()