from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    description_pkg = get_package_share_directory('kr_robot_description')

    xacro_file = os.path.join(description_pkg, 
                              'kr810',
                              'urdf', 
                              'kr810_description_1.urdf.xacro')
    
    controller_config = os.path.join(description_pkg, 
                                     'kr810',
                                     'config', 
                                     'kr810_controllers.yaml')

    robot_description = {'robot_description': Command(['xacro ', xacro_file])}

    return LaunchDescription([
        DeclareLaunchArgument("x", default_value="0.0"),
        DeclareLaunchArgument("y", default_value="0.0"),
        DeclareLaunchArgument("z", default_value="0.0"),

        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[robot_description, controller_config, {'use_sim_time': True}],
            output='screen'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[robot_description],
            output='screen'
        ),

        # Spawn robot in Gazebo
        Node(
            package="gz_ros2_control",
            executable="spawn_entity.py",
            arguments=[
                "-entity", "kr810",
                "-topic", "robot_description",
                "-x", LaunchConfiguration("x"),
                "-y", LaunchConfiguration("y"),
                "-z", LaunchConfiguration("z")
            ],
            output="screen"
        )
    ])
