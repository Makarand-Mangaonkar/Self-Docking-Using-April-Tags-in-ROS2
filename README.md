# Self-Docking-Using-April-Tags-in-ROS2

# Goal: 
Demonstrate your ability to:
- Detect and track a docking station in real time.
- align itself accurately based on the tag’s position.
- Move forward, adjust orientation, and dock autonomously.


# Prerequisites:

Before using, ensure you have the following dependencies installed:

- ROS2 `Humble` distribution
- Additional packages:
  - `gazebo*`
  - `xacro`
  - `rmw_cyclonedds_cpp`
  - `nav2*`

>If you are using **`binary installation`**, you can install these packages using `apt`. 

>If you are using **`source installation`**, make sure you have built your ROS2 Humble source folder, and you'll need the `behaviours_tree_v3` package from the GitHub v3.8 branch. 


# Installation

To get started, make a workspace and clone the repository:

```bash
mkdir -p docking_ws/src
```

```bash
cd docking_ws/src/
```

```bash[
git clone https://github.com/Makarand-Mangaonkar/docking_robotics.git](https://github.com/Makarand-Mangaonkar/Self-Docking-Using-April-Tags-in-ROS2.git)
```

# Build the repository using the following command:

```bash
cd docking_ws/
```

```bash
colcon build --symlink-install
```

>Make sure you have sourced ROS2 Humble in your terminal before building.

```bash
source install/setup.bash
```


# Usage

  - Source your build workspace every time before running any files or nodes:

    ```bash
    source install/setup.bash
    ```

  - To launch the Gazebo simulation and spawn the robot with all plugins:

    ```bash
    ros2 launch mack_bringup gazebo_bringup.launch.py
    ```

  - For SLAM (Simultaneous Localization and Mapping) functionality:

    ```bash
    ros2 launch mack_navigation slam.launch.py
    ```

  - For launching navigation:

    ```bash
    ros2 launch mack_navigation navigation.launch.py
    ```
   
    Map name: warehouse
 
# To run Docking :    
   
  - 
  
    ```bash
    ros2 launch mack_navigation apriltag_navigation.launch.py 
    ```
    
    
    
    

    
    
   
