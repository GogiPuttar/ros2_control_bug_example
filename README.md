# ros2_control_bug_example
Minimal example with docker container for illustrating bug with ros2_control bug: https://github.com/ros-controls/ros2_control/issues/2309

## Overview
This spins up a simple environment with ROS 2 Jazzy and Gazebo Harmonic (8.9.0). 
The following instructions help recreate the error messages I'm seeing, particularly the very fishy:
```
[INFO] [1755800831.439939591] [controller_manager]: Loading controller : 'joint_state_broadcaster' of type 'joint_state_broadcaster/JointStateBroadcaster'
[INFO] [1755800831.440111638] [controller_manager]: Loading controller 'joint_state_broadcaster'
[INFO] [1755800831.451934186] [controller_manager]: Controller 'joint_state_broadcaster' node arguments: --ros-args --params-file -p use_sim_time:=true --param use_sim_time:=true 
[ERROR] [1755800831.453019700] [controller_manager]: Caught exception of type : N6rclcpp10exceptions22RCLInvalidROSArgsErrorE while initializing controller 'joint_state_broadcaster': failed to parse arguments: Couldn't parse params file: '--params-file -p'. Error: Error opening YAML file, at ./src/parser.c:271, at ./src/rcl/arguments.c:415
```

<br>

## Requirements
- Intel Mesa GPU (for rendering Gazebo Harmonic)
- `docker` and `docker compose`:
  ```
  docker --version        # should be >= 20.10
  docker compose version  # should return 1.25.5+ / Compose v2+. Not to be confused with `docker-compose --version`!
  ```
- Feel free to edit the permissions in `docker/ros-example-env/docker-compose.yml` to best fit your requirements.
The current setup is just tailored to my needs :)

<br>

## Instructions

- Build docker container (might take ~10 mins):
  ```
  cd docker/ros-example-env
  docker compose build --no-cache
  ```

- Run the docker container:
  ```
  docker compose run --rm ros-example-env
  ```
  You should see something like:
  ```
  adityanair@pop-os:~/ros2_control_bug/ros2_control_bug_example/docker/ros-example-env$ docker compose run --rm ros-example-env
  Agent pid 21
  Identity added: /root/.ssh/id_ed25519 (dev-container-key)
  root@pop-os:~/ros2_control_bug_example(main)# 
  ```
- Build the workspace:
  ```
  colcon build
  source install/setup.bash
  ```
- Spin up two more sourced terminals:
  In two new terminals run;
  ```
  docker compose exec ros-example-env bash
  ```
- In one of these terminals run:
  ```
  gz sim -v4 empty.sdf
  ```
- In the second terminal run:
  ```
  ros2 launch example_pkg sim.launch.py
  ```
  
  <details>
  <summary>Gazebo should print:</summary>

  ```
  [INFO] [1755801818.126504953] [gz_ros_control]: [gz_ros2_control] Fixed joint [joint_world] (Entity=31)] is skipped
  [INFO] [1755801818.127807861] [gz_ros_control]: Loading controller_manager
  [INFO] [1755801818.146690635] [controller_manager]: Using ROS clock for triggering controller manager cycles.
  [INFO] [1755801818.154528921] [controller_manager]: Subscribing to '/robot_description' topic for robot description.
  [WARN] [1755801818.158432964] [gz_ros_control]: Waiting RM to load and initialize hardware...
  [INFO] [1755801818.291384124] [controller_manager]: Received robot description from topic.
  [INFO] [1755801818.300345944] [gz_ros_control]: The position_proportional_gain has been set to: 0.1
  [INFO] [1755801818.300484028] [gz_ros_control]: Loading joint: joint_1
  [INFO] [1755801818.300498801] [gz_ros_control]: 	State:
  [INFO] [1755801818.300509092] [gz_ros_control]: 		 position
  [INFO] [1755801818.300549160] [gz_ros_control]: 		 found initial value: 1.000000
  [INFO] [1755801818.300568052] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.300588481] [gz_ros_control]: 	Command:
  [INFO] [1755801818.300601252] [gz_ros_control]: 		 position
  [INFO] [1755801818.300656463] [gz_ros_control]: Loading joint: joint_2
  [INFO] [1755801818.300666906] [gz_ros_control]: 	State:
  [INFO] [1755801818.300673840] [gz_ros_control]: 		 position
  [INFO] [1755801818.300693408] [gz_ros_control]: 		 found initial value: -1.000000
  [INFO] [1755801818.300704014] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.300718100] [gz_ros_control]: 	Command:
  [INFO] [1755801818.300727849] [gz_ros_control]: 		 position
  [INFO] [1755801818.300762774] [gz_ros_control]: Loading joint: joint_3
  [INFO] [1755801818.300773448] [gz_ros_control]: 	State:
  [INFO] [1755801818.300783011] [gz_ros_control]: 		 position
  [INFO] [1755801818.300795434] [gz_ros_control]: 		 found initial value: 1.000000
  [INFO] [1755801818.300806539] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.300818969] [gz_ros_control]: 	Command:
  [INFO] [1755801818.300829475] [gz_ros_control]: 		 position
  [INFO] [1755801818.300861960] [gz_ros_control]: Loading joint: joint_4
  [INFO] [1755801818.300870416] [gz_ros_control]: 	State:
  [INFO] [1755801818.300878574] [gz_ros_control]: 		 position
  [INFO] [1755801818.300888409] [gz_ros_control]: 		 found initial value: 1.000000
  [INFO] [1755801818.300897160] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.300909637] [gz_ros_control]: 	Command:
  [INFO] [1755801818.300918791] [gz_ros_control]: 		 position
  [INFO] [1755801818.300960393] [gz_ros_control]: Loading joint: joint_5
  [INFO] [1755801818.300979394] [gz_ros_control]: 	State:
  [INFO] [1755801818.300994186] [gz_ros_control]: 		 position
  [INFO] [1755801818.301005583] [gz_ros_control]: 		 found initial value: 1.000000
  [INFO] [1755801818.301015100] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.301024479] [gz_ros_control]: 	Command:
  [INFO] [1755801818.301032574] [gz_ros_control]: 		 position
  [INFO] [1755801818.301069825] [gz_ros_control]: Loading joint: joint_6
  [INFO] [1755801818.301082920] [gz_ros_control]: 	State:
  [INFO] [1755801818.301094002] [gz_ros_control]: 		 position
  [INFO] [1755801818.301104385] [gz_ros_control]: 		 found initial value: 1.000000
  [INFO] [1755801818.301112261] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.301119255] [gz_ros_control]: 	Command:
  [INFO] [1755801818.301127653] [gz_ros_control]: 		 position
  [INFO] [1755801818.301156282] [gz_ros_control]: Loading joint: joint_7
  [INFO] [1755801818.301165928] [gz_ros_control]: 	State:
  [INFO] [1755801818.301172385] [gz_ros_control]: 		 position
  [INFO] [1755801818.301182199] [gz_ros_control]: 		 found initial value: 1.000000
  [INFO] [1755801818.301191600] [gz_ros_control]: 		 velocity
  [INFO] [1755801818.301204171] [gz_ros_control]: 	Command:
  [INFO] [1755801818.301212803] [gz_ros_control]: 		 position
  [INFO] [1755801818.301394920] [controller_manager]: Initialize hardware 'GazeboSimSystem' 
  [WARN] [1755801818.301441718] [controller_manager]: Executor is not available during hardware component initialization for 'GazeboSimSystem'. Skipping node creation!
  [INFO] [1755801818.301552557] [controller_manager]: Successful initialization of hardware 'GazeboSimSystem'
  [INFO] [1755801818.301873130] [resource_manager]: 'configure' hardware 'GazeboSimSystem' 
  [INFO] [1755801818.301889322] [gz_ros_control]: System Successfully configured!
  [INFO] [1755801818.301903466] [resource_manager]: Successful 'configure' of hardware 'GazeboSimSystem'
  [INFO] [1755801818.301925191] [resource_manager]: 'activate' hardware 'GazeboSimSystem' 
  [INFO] [1755801818.301949480] [resource_manager]: Successful 'activate' of hardware 'GazeboSimSystem'
  [INFO] [1755801818.302089136] [controller_manager]: Resource Manager has been successfully initialized. Starting Controller Manager services...
  [Dbg] [SystemManager.cc:80] Loaded system [gz_ros2_control::GazeboSimROS2ControlPlugin] for entity [10]
  [Dbg] [UserCommands.cc:1318] Created entity [10] named [kr810]
  [Dbg] [SimulationRunner.cc:560] Exiting postupdate worker thread (0)
  [Dbg] [SimulationRunner.cc:560] Exiting postupdate worker thread (1)
  [Dbg] [SimulationRunner.cc:533] Creating PostUpdate worker threads: 4
  [Dbg] [SimulationRunner.cc:544] Creating postupdate worker thread (0)
  [Dbg] [SimulationRunner.cc:544] Creating postupdate worker thread (1)
  [Dbg] [SimulationRunner.cc:544] Creating postupdate worker thread (2)
  [WARN] [1755801820.177720354] [gz_ros_control]:  Desired controller update period (0.0025 s) is slower than the gazebo simulation period (0 s).
  ```
  </details>
- In the third terminal run:
  ```
  ros2 run controller_manager spawner joint_state_broadcaster
  ```
  <details>
  <summary>You should immediately see:</summary>
  
  ```
  [FATAL] [1755801979.122976081] [spawner_joint_state_broadcaster]: Failed loading controller joint_state_broadcaster
  [ros2run]: Process exited with failure 1
  ```
  </details>

  <details>
  <summary>And in the gazebo terminal you should see:</summary>

  ```
  [INFO] [1755801979.075956695] [controller_manager]: Loading controller : 'joint_state_broadcaster' of type 'joint_state_broadcaster/JointStateBroadcaster'
  [INFO] [1755801979.076100283] [controller_manager]: Loading controller 'joint_state_broadcaster'
  [INFO] [1755801979.086769039] [controller_manager]: Controller 'joint_state_broadcaster' node arguments: --ros-args --params-file -p use_sim_time:=true --param use_sim_time:=true 
  [ERROR] [1755801979.087494038] [controller_manager]: Caught exception of type : N6rclcpp10exceptions22RCLInvalidROSArgsErrorE while initializing controller 'joint_state_broadcaster': failed to parse arguments: Couldn't parse params file: '--params-file -p'. Error: Error opening YAML file, at ./src/parser.c:271, at ./src/rcl/arguments.c:415
  ```
  </details>
  
<br>

## Quick Links to relevant files
- Launch file: [`sim.launch.py`](https://github.com/GogiPuttar/ros2_control_bug_example/blob/main/src/example_pkg/launch/sim.launch.py)
- Xacro: [`kr810_description.urdf.xacro`](https://github.com/GogiPuttar/ros2_control_bug_example/blob/main/external/kr_ros2/kr_robot_description/kr810/urdf/kr810_description.urdf.xacro)
- Config file(s) (The current example uses `kr810_controllers_1.yaml`) but I'm not sure what is the right way to structure this file so I have two:
  - [`kr810_controllers_1.yaml`](https://github.com/GogiPuttar/ros2_control_bug_example/blob/main/external/kr_ros2/kr_robot_description/kr810/config/kr810_controllers_1.yaml)
  - [`kr810_controllers.yaml`](https://github.com/GogiPuttar/ros2_control_bug_example/blob/main/external/kr_ros2/kr_robot_description/kr810/config/kr810_controllers.yaml)

Thanks for looking into this :)