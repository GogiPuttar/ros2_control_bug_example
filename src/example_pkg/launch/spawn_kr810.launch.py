from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    kr_desc_pkg = get_package_share_directory("kr_robot_description")
    xacro_path = os.path.join(kr_desc_pkg, "kr810", "urdf", "kr810_description.urdf.xacro")

    robot_description = ParameterValue(
        Command(["xacro ", xacro_path]),
        value_type=str
    )

    return LaunchDescription([
        DeclareLaunchArgument("x", default_value="0.0"),
        DeclareLaunchArgument("y", default_value="0.0"),
        DeclareLaunchArgument("z", default_value="0.0"),

        # Spawn robot in Gazebo
        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
                "-name", "kr810",
                "-x", LaunchConfiguration("x"),
                "-y", LaunchConfiguration("y"),
                "-z", LaunchConfiguration("z"),
                "-topic", "robot_description"
            ],
            output="screen"
        ),

        # Robot state publisher (can start immediately)
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen"
        ),
    ])
