from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='camera_test', executable='detect_human', name='detect_human'),
        Node(package='camera_test', executable='detect_object', name='detect_object'),
        Node(package='camera_test', executable='visualize', name='visualize'),
        Node(package='camera_test', executable='camera_ui', name='camera_ui'),
    ])
