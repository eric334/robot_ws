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
sudo userdel -f aion
sudo userdel -f ubuntu
sudo dpkg -i nomachine_7.7.4_1_arm64.deb
sudo apt install ncdu
sudo apt-get --purge remove aisleriot brltty duplicity empathy empathy-common example-content gnome-accessibility-themes gnome-contacts gnome-mahjongg gnome-mines gnome-orca gnome-screensaver gnome-sudoku gnome-video-effects gnomine landscape-common libreoffice-avmedia-backend-gstreamer libreoffice-base-core libreoffice-calc libreoffice-common libreoffice-core libreoffice-draw libreoffice-gnome libreoffice-gtk libreoffice-impress libreoffice-math libreoffice-ogltrans libreoffice-pdfimport libreoffice-style-galaxy libreoffice-style-human libreoffice-writer libsane libsane-common mcp-account-manager-uoa python3-uno rhythmbox rhythmbox-plugins rhythmbox-plugin-zeitgeist sane-utils shotwell shotwell-common telepathy-gabble telepathy-haze telepathy-idle telepathy-indicator telepathy-logger telepathy-mission-control-5 telepathy-salut totem totem-common totem-plugins printer-driver-brlaser printer-driver-foo2zjs printer-driver-foo2zjs-common printer-driver-m2300w printer-driver-ptouch printer-driver-splix unity
sudo apt-get --purge remove cuda-*

Running nodes individually:
rosrun roboclaw_node roboclaw.launch
rosrun usb_cam usb_cam_node
rosrun rplidar_ros rplidarNodeClient
rosrun joy joy_node

After ROS file edit:
catkin_make && source ~/robot_ws/devel/setup.bash
