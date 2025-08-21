from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    

    pkg_share = get_package_share_directory("example_pkg")
    model_file = os.path.join(pkg_share, "models", "table", "model.sdf")

    # model_path = LaunchConfiguration("model_path")
    model_name = LaunchConfiguration("model_name")
    x = LaunchConfiguration("x")
    y = LaunchConfiguration("y")
    z = LaunchConfiguration("z")

    return LaunchDescription([
        DeclareLaunchArgument("model_path", default_value="models/table"),
        DeclareLaunchArgument("model_name", default_value="table"),
        DeclareLaunchArgument("x", default_value="0.0"),
        DeclareLaunchArgument("y", default_value="0.0"),
        DeclareLaunchArgument("z", default_value="0.0"),

        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
                "-name", model_name,
                "-x", x,
                "-y", y,
                "-z", z,
                "-file", model_file
            ],
            output="screen"
        )
    ])
