REFLASH PROCESS
Install jetpack 3.3 on robot using 16.04 virtual machine
Place tx2 gold image in bootloader folder

Run command
cd Downloads/64_TX2/Linux_for_Tegra/
sudo ./flash.sh -r -k APP jetson-tx2 mmcblk0p1

After installation:

Copy the nomachine deb file into home

Run the following in terminal:
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
sudo apt-get update
sudo apt-get upgrade
git clone git@github.com:eric334/robot_ws.git
echo 'source ~/robot_ws/devel/setup.bash' >> .bashrc
sudo adduser $USER dialout
sudo userdel -r -f aion
sudo userdel -r -f ubuntu
sudo dpkg -i nomachine_7.7.4_1_arm64.deb

Running nodes individually:
rosrun roboclaw_node roboclaw.launch
rosrun usb_cam usb_cam_node
rosrun rplidar_ros rplidarNodeClient
rosrun joy joy_node

After ROS file edit:
catkin_make && source ~/robot_ws/devel/setup.bash
