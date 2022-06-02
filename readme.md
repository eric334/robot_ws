# Capstone AION UGV ROS Catkin Workspace

## High level setup for AION R1
If Xenial (Ubu 16.04) AION image is already installed, skip the first step and login with u: nvidia p: nvidia
- Flash AION R1 TX2 with AION Gold Image
- Install ROS Kinetic Desktop
- Clone this repo
- Configure device ports in robot_jumbo.launch, see below
- <code>roslaunch robot_jumbo.launch</code> in terminal

## Configuring Device Ports
Serial ports are randomized on boot, so it is necessary to assign each device the serial <code>dev</code>
- For each serial device
  - Unplug and replug device from board
  - Use <code>dmesg | grep tty</code> to find the latest attached port
  - Use this <code>dev</code> in <code>roslaunch robot_jumbo.launch</code>
