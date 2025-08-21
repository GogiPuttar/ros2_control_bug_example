FROM ubuntu:24.04

# Set non-interactive frontend
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Basic setup and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common \
    build-essential \
    git \
    wget \
    mesa-utils \
    libgl1 \
    libglx-mesa0 \
    libgl1-mesa-dri \
    libglu1-mesa \
    ca-certificates \
    && locale-gen en_US en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Add ROS 2 Jazzy repo
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | gpg --dearmor -o /etc/apt/keyrings/ros-archive-keyring.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2.list

# Add Gazebo Harmonic repo
RUN curl -sSL https://packages.osrfoundation.org/gazebo.key | gpg --dearmor -o /usr/share/keyrings/gazebo.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/gazebo.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list

# Install ROS 2 Jazzy and Gazebo Harmonic
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-desktop \
    gz-harmonic \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rosdep init \
    && rosdep update \
    && rm -rf /var/lib/apt/lists/*

# Additional dependencies that are continuously discovered (TODO: maybe roll into another RUN for crispness after development is at a final stage and a tag/image is about to be published)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3.12-venv \
    bash-completion \
    command-not-found \
    less \
    apt-cacher \
    nano \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-tf-transformations \
    ros-jazzy-ros2-control \
    ros-jazzy-controller-manager \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    gitk && \
    pip install --break-system-packages --upgrade paramiko

# Additional dependencies that i am unsure of (TODO: maybe roll into another RUN for crispness after development is at a final stage and a tag/image is about to be published)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-gz-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-actuator-msgs \
    ros-jazzy-gps-msgs \
    ros-jazzy-gz-ros2-control-demos \
    ros-jazzy-ros-gz-bridge

# Realsense stuff
RUN apt-get update && apt-get install -y --no-install-recommends \
    usbutils \
    file \
    ros-jazzy-realsense2-camera \
    ros-jazzy-vision-msgs \
    ros-jazzy-topic-tools && \
    pip install --break-system-packages --upgrade pyrealsense2

# DDS Installs for cross container/distro ROS 2 usage 
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-rmw-implementation \
    ros-jazzy-rmw-cyclonedds-cpp

# Clean up bash history and temporary files
RUN rm -rf /tmp/* /var/tmp/* ~/.cache

# Copy custom .bashrc into root's home
SHELL ["/bin/bash", "-c"]
COPY .bashrc /root/.bashrc
COPY git_config_setup.sh /root/git_config_setup.sh

# Set workspace
WORKDIR /root/ros2_control_bug_example
CMD ["bash"]
