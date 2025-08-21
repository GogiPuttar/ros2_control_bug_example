from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    kr_desc_pkg = get_package_share_directory("kr_robot_description")
    xacro_path = os.path.join(kr_desc_pkg, "kr810", "urdf", "kr810_description.urdf.xacro")
    controllers_yaml = os.path.join(kr_desc_pkg, "kr810", "config", "kr810_controllers_1.yaml")

    robot_description = ParameterValue(
        Command([
            "xacro ", xacro_path,
            " controllers_file:=", controllers_yaml
        ]),
        value_type=str
    )

    return LaunchDescription([
        # ONLY robot_state_publisher gets use_sim_time
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}, {"use_sim_time": True}],
            output="screen",
        ),

        # Gazebo will launch controller_manager via the gz_ros2_control plugin
        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=["-name", "kr810", "-topic", "/robot_description"],
            output="screen",
        ),

        # Node(
        #     package="controller_manager",
        #     executable="spawner",
        #     arguments=["joint_state_broadcaster", "-c", "/controller_manager"],
        #     additional_arguments=["--ros-args"],
        #     output="screen",
        # )

    ])
