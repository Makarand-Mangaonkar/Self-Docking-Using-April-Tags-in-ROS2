import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Get the path to the package share directory
    apriltag_ros_share_dir = get_package_share_directory('apriltag_ros')

    # Get the path to the tags_36h11.yaml file
    tags_36h11_yaml_file = os.path.join(apriltag_ros_share_dir, 'cfg', 'tags_36h11.yaml')

    # Create the launch description
    launch_description = LaunchDescription([
        Node(
            package='apriltag_ros',
            executable='apriltag_node',
            name='apriltag_node',
            output='screen',
            remappings=[
                ('image_rect', '/camera/rgb/image_rect_color'),
                ('camera_info', '/camera/rgb/camera_info')
            ],
            parameters=[
                {'params_file': tags_36h11_yaml_file}
            ]
        ),
        Node(
            package='mack_navigation',
            executable='apriltag_detection.py',
            output='screen',
        )
    ])

    return launch_description
