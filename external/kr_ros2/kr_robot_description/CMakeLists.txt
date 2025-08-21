cmake_minimum_required(VERSION 3.5)
project(kr_robot_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY 
  kr810/meshes kr810/urdf kr810/rviz kr810/config
  DESTINATION share/${PROJECT_NAME}/kr810
)

ament_package()
