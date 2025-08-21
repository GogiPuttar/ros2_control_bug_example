from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    kr_desc_pkg = get_package_share_directory("kr_robot_description")
    xacro_path = os.path.join(kr_desc_pkg, "kr810", "urdf", "kr810_description_1.urdf.xacro")
    controller_yaml = os.path.join(kr_desc_pkg, "kr810", "config", "kr810_controllers.yaml")

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

        # Delay ros2_control_node to ensure robot is spawned
        TimerAction(
            period=2.0,
            actions=[
                Node(
                    package="controller_manager",
                    executable="ros2_control_node",
                    parameters=[
                        {"robot_description": robot_description},
                        controller_yaml
                    ],
                    output="screen"
                )
            ]
        ),

        # Robot state publisher (can start immediately)
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen"
        ),

        # Delay controller spawners to after ros2_control is running
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["joint_state_broadcaster", "--controller-manager-timeout", "50"],
                    output="screen"
                ),
                Node(
                    package="controller_manager",
                    executable="spawner",
                    arguments=["effort_trajectory_controller", "--controller-manager-timeout", "50"],
                    output="screen"
                )
            ]
        ),
    ])
