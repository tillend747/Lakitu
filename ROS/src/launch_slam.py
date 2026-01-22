#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # --- Parameter für RPLIDAR ---
    port = '/dev/ttyUSB0'  # Passe ggf. an
    baudrate = 256000

    # --- Nodes ---

    # RPLIDAR Node
    rplidar_node = Node(
        package='rplidar_ros',
        executable='rplidarNode',
        name='rplidar_node',
        output='screen',
        parameters=[{
            'serial_port': port,
            'serial_baudrate': baudrate,
            'frame_id': 'laser',
            'inverted': False,
            'angle_compensate': True
        }]
    )

    # Static TF: laser -> base_link
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='laser_to_base_link_tf',
        arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'laser'],
        output='screen'
    )

    # SLAM Toolbox Node
    slam_node = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[{
            'use_sim_time': False
        }],
        remappings=[
            ('scan', '/scan')
        ]
    )

    # RViz (optional)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(
            os.path.dirname(__file__), 'rplidar_slam.rviz')]
    )

    return LaunchDescription([
        rplidar_node,
        static_tf,
        slam_node,
        rviz_node
    ])
