#!/usr/bin/python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_prefix

def generate_launch_description():

  pkg_mack_gazebo = get_package_share_directory('mack_gazebo')
  pkg_mack_description = get_package_share_directory('mack_description')

  gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(pkg_mack_gazebo, 'launch', 'start_world.launch.py'),
    )
  ) 
  
  state_pub = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(pkg_mack_description, 'launch', 'publish_urdf.launch.py'),
    )
  )

  spawn = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(pkg_mack_gazebo, 'launch', 'spawn_robot_description.launch.py'),
    )
  ) 

  return LaunchDescription([
    gazebo,
    state_pub,
    spawn
  ])