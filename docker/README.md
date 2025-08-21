# Artifact of my actual repo, not relevant to the ros2_control bug!
# futur_docker
Standardized Docker environments for cross platform use.

## Goals
Make two separate docker environments, namely
- `ros-gazebo`: Minimal general purpose environment prioritizing utility over multiple platforms. 
  - Ubuntu 24.04
  - ROS 2 Jazzy
  - Gazebo Harmonic
  - Currently only relies on llvmpipe for graphics, to prioritize being general purpose
  
- `ros-gazebo-nvidia`: Dedicate environment for use on Linux systems having the required NVIDIA drivers and CUDA version. 
  - Ubuntu 24.04
  - ROS 2 Jazzy
  - Gazebo Harmonic
  - Base image: nvidia/cuda:12.9.1-cudnn-devel-ubuntu24.04
  - CUDA Version >= 12.9.1
  - NVIDIA GPU compute (and possibly graphics) acceleration properly setup

Automated build testing via GitHub actions will also be added to CPU test (and possibly even GPU test) these environments across various platforms, on and outside of the cloud.

<br>

## Instructions

**1. Set up [`FuturHub`](https://github.com/FuturHandRobotics/FuturHub) repo:**

  - Follow the setup instructions in [`FuturHub/README.md`](https://github.com/FuturHandRobotics/FuturHub/blob/main/README.md)

**2. Install docker**

- If not already installed:
  ```
  curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker $USER && newgrp docker
  ```

- If you already have `docker` installed and added, and you just want `docker compose`:

  1. Check if they have an installable version for your system by inspecting: https://github.com/docker/compose/releases/latest/

  2. Install the required version as a plugin. Eg. for `linux-x86-64`:
      ```
      mkdir -p ~/.docker/cli-plugins && \
      curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose && \
      chmod +x ~/.docker/cli-plugins/docker-compose
      ```

- Finally, confirm `docker` and `docker compose` versions:
  ```
  docker --version        # should be >= 20.10
  docker compose version  # should return 1.25.5+ / Compose v2+. Not to be confused with `docker-compose --version`!
  ```

**3. Build `ros-gazebo` Docker container**

- Before building, run this on your system to avoid seeing annoying deprecation warnings:
  ```
  pip install --upgrade cryptography paramiko
  ```
- Change to required docker container's directory:
  ```
  cd FuturHub/futur_docker/ros-gazebo
  ```
- First time build:
  ```
  docker compose up --build
  ```

  Rebuild (without cache, slower but more stable):
  ```
  docker compose build --no-cache
  ```

- If you see:
  ```
  KeyError: 'ContainerConfig'
  ```
  while building, refresh the build with:
  ```
  docker compose down --remove-orphans
  ```
  and try building again.

**4. Configure Git (Necessary for building the container):**

- Create a dedicated key for development within the container
  ```
  ssh-keygen -t ed25519 -C "dev-container-key" -f ~/.ssh/id_ed25519_devcontainer
  ```

- Add the public key (output) from:
  ```
  cat ~/.ssh/id_ed25519_devcontainer.pub
  ```
  into your list of authentication keys: https://github.com/settings/keys

- Create a `futur_docker/ros-gazebo/git_config_setup.sh` based off `futur_docker/ros-gazebo/git_config_setup.sh`:
  
  In the `futur_docker/ros-gazebo` directory:
  ```
  cp git_config_setup.sh.example git_config_setup.sh
  ```

- Fill in your name and GitHub email in `futur_docker/ros-gazebo/git_config_setup.sh`:
  ```
  # Configure Git
  git config --global user.name "<Your Name>"
  git config --global user.email "<Your email>"
  ```
- Note: Confirm that `~/.ssh/id_ed25519_devcontainer` has read and write permissions:
  `ls -l ~/.ssh/id_ed25519_devcontainer`
  ```
  -rw-------  # or 600
  ```
  if not:
  ```
  chmod 600 ~/.ssh/id_ed25519_devcontainer
  ```

- Note: Since docker runs as `root` while the host does not, running the container can overwrite `.gitobjects` to no longer allow host any priviliges. 
This can be easily fixed by running the following command on the host, post-hoc:
  ```
  sudo chown -R $(whoami):$(whoami) ~/FuturHub/.git
  ```
  TODO: A conclusive fix for this. For now, just try to keep all Git development within the container. This should not mess with VS Code's Git tracking. Please report if it does!

**5. Install Intel Realsense dependencies on Host**
- Realsense [install instructions for Linux host](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md).
    In summary:

    ```
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6B0FC61
    sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo $(lsb_release -cs) main"
    sudo apt update
    sudo apt install librealsense2-dkms librealsense2-utils librealsense2-dev
    ```
   Make sure to plug the RealSense into a USB 3.0 (blue) port, and use a USB data cable!
   Also, ensure that the camera is not replugged while the docker container is running (TODO: permanent fix for this).

**6. Run `ros-gazebo` Docker container**
  
**Standard mode of operation**, for switching in and out of the docker container:
- Run container for testing:
  ```
  xhost +local:root
  docker compose run --rm ros-gazebo
  xhost -local:root # after your session is over
  ```
- Open running container in a different terminal:
  ```
  docker compose exec ros-gazebo bash
  ```
- Exit container:
  ```
  exit
  ```
<br>

## Testing 
(July 22nd, 2025)

In order to be functional, the docker container must satisfy the following test cases:

1. **Build checks:**
   
    On your host:
    ```
    cd FuturHub/futur_docker/ros-gazebo
    pip install --upgrade cryptography paramiko
    docker compose up --build
    ```
    **Passes:**
    - Builds fully
    - No cryptogrpahy deprecation warning
    - No attribute `version` is obsolete warning

2. **Setup checks:**
    ```
    xhost +local:root
    docker compose run --rm ros-gazebo
    xhost -local:root # after your session is over
    ```
    **Passes:**
    - No cryptography deprecation warning on startup
    - You see `[setup YOLOv8 venv] Environment is healthy. Nothing to do.`
    - `pwd`
      ```
      /root/FuturHub
      ```
    - `ls`
      ```
      build  futur_docker  log  setup.sh  venvs  external  install  README.md  src
      ```
      or
      ```
      futur_docker  setup.sh  venvs  external  README.md  src
      ```
    - `glxinfo | grep "OpenGL renderer"`
      ```
      OpenGL renderer string: Mesa Intel(R) Graphics (RPL-S)
      ```

3. **ROS 2 and Gazebo checks:**
   
    **Passes:**
    - `echo $ROS_DISTRO`
      ```
      jazzy
      ```
    - `ros2 doctor`
      ```
      ...

      All 5 checks passed
      ```
    - `gz sim --versions`
      ```
      8.x.x
      ```
    - `rviz2` RViz shows up
    - `gz sim` Gazebo shows up
    - `echo $LIBGL_ALWAYS_SOFTWARE`
      ```
      0
      ```
    - `echo $LD_LIBRARY_PATH`
      ```
      ...:/opt/ros/jazzy/opt/rviz_ogre_vendor/lib:
      ```
    - `ros2 pkg list | grep ros_gz_sim`
      ```
      ros_gz_sim
      ```

4. **Quality of life improvements/checks:**
   
    **Passes:**
    - Apt tab completion works: Eg. `apt install ros-jazzy-t<TAB><TAB>` shows all installable packages with that substring.
    - Git bash completion works: Eg. `git <TAB><TAB>`.
    - History search filter works: Eg. `ros2 ^[[A` only shows terminal history beginning with `ros2`.
    - `ls /tmp` returns empty.
    - `exit` is clean with no logs.

5. **Git config checks:**
   
    **Passes:**
   - `git config --global user.name`
     ```
     <Your Name>
     ```
   - `git config --global user.email`
     ```
     <Your email>
     ```
   - `git config --global init.defaultBranch`
     ```
     main
     ```
   - `ssh -T git@github.com`
     ```
     Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
     ```

6. **Realsense checks:**
   
   **Passes:**
   - `realsense-viewer` opens up toggleable realsense camera.
   
