from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        # IMU Node
        Node(
            package='imu_bridge_pkg',
            executable='imu_serial_bridge',
            name='imu_bridge',
            output='screen'
        ),

        # TF: base_link → imu_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'imu_link']
        ),

        # Lidar Node (RPLIDAR)
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            name='lidar',
            output='screen'
        ),

        # TF: base_link → laser
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0.05', '0', '0', '0', 'base_link', 'laser']
        ),

        # EKF
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter',
            parameters=['/home/till-kappeler/lakitu/src/imu_bridge_pkg/config/ekf.yaml'],
            output='screen'
        ),

        # SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam',
            output='screen',
        )
    ])
