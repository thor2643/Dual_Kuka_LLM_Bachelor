# Dual_Kuka_LLM_Bachelor
This repository contains the source code for our bachelor project in robotics at Aalborg University, and explores the integration of ... to make automation more intuitive for operators. The GitHub contains all the code produced throughout the project period, from ... to ...

This project is a continuation of the work performed during the 5th semester. The GitHub page for the 5th semester project can be found here: 
- [P5 Project](https://github.com/thor2643/P5-Kuka-Dual-Arm)

## Quick Start
This quick-start guide assumes a clean installation of Ubuntu 22.04 LTS (Jammy Jellyfish) along with ROS 2 Humble. If either is not yet set up, you can refer to the following resources:
- [Ubuntu 22.04 LTS](https://medium.com/@maheshdeshmukh22/how-to-install-ubuntu-22-04-lts-on-virtualbox-in-windows-11-6c259ce8ef60)
- [ROS2 - Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

If your system crashes or you need to switch terminals at any point, ensure you re-run the following command:

    source /opt/ros/humble/setup.bash
    
Before starting the installation of this project, we recommend grabbing a snack and a beverage. The process will take at least 30 minutes.

1. Install ROS 2 development tools

    ```shell
    sudo apt install ros-dev-tools
    ```

2. Create a workspace, clone, and install dependencies

    ```shell
    cd ~
    source /opt/ros/humble/setup.bash
    git clone https://github.com/thor2643/Dual_Kuka_LLM_Bachelor.git
    cd Dual_Kuka_LLM_Bachelor/p6_ws
    sudo rosdep init
    rosdep update
    rosdep install --from-paths src -i -r -y
    ```

3. Installing colcon mixin and pip (Needed for Moveit2)

    ```shell
    sudo apt install python3-colcon-common-extensions
    sudo apt install python3-colcon-mixin
    sudo apt install python3-pip
    sudo apt-get install portaudio19-dev python-all-dev
    colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
    colcon mixin update default
    sudo apt install python3-vcstool
    ```

4. Installing python libraries

    ```shell
    cd ~/Dual_Kuka_LLM_Bachelor
    pip install -r requirements.txt
    ```

5. Adding an API key for Janise

   ```shell
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/robutler/janise
    nano API_KEY.json
    # Added your API Key for GPT following the format
    # {
    #     "API_KEY": "Insert your API Key here"
    # }
    # Remember to write the file, ctrl + s then ctrl + x
    ```

This next step is without a doubt the hardest, and may require manuel intervention. If the quickstart guide fails, confer to: [GraspNet-Baseline](https://github.com/graspnet/graspnet-baseline)

For transparency, our GraspNet-Baseline was built with the following: Nvidia Driver 550.144.03, Cuda 11.8, cuDNN 8700, Torch 2.0.0+cu118 - 4060 Laptop GPU. If you have any other version of these installed, you may have to build GraspNet-Baseline from scratch.
    
6. Building GraspNet-Baseline (The quick way)

   ```shell
    pip install gdown
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/dataset
    gdown 1DcjGGhZIJsxd61719N0iWA7L6vNEK0ci
    tar -xvf tolerance.tar
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/graspnetAPI
    pip install .
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet
    mkdir -p logs/log_kn
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/logs/log_kn
    gdown 1hd0G8LN6tRpi4742XOTEisbTXNZ-1jmk
    ```

7. Building GraspNet-Baseline (From scratch)

   ```shell
    # Start by building GraspNet-Baseline
    
    pip install gdown
    cd ~
    git clone https://github.com/graspnet/graspnet-baseline.git
    cd ~/graspnet-baseline/pointnet2
    python setup.py install
    cd ~/graspnet-baseline/knn
    python setup.py install
    cd ~
    git clone https://github.com/graspnet/graspnetAPI.git
    cd ~/graspnetAPI
    pip install .
    cd ~/graspnet-baseline/dataset
    gdown 1DcjGGhZIJsxd61719N0iWA7L6vNEK0ci
    tar -xvf tolerance.tar
    cd ~/graspnet-baseline
    mkdir -p logs/log_kn
    cd ~/graspnet-baseline/logs/log_kn
    gdown 1hd0G8LN6tRpi4742XOTEisbTXNZ-1jmk
    
    # Now you have all the files, and just need them to follow the structure used in our ROS2 implementation
    
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet
    rm -rf dataset graspnetAPI knn models pointnet2 utils
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/graspnet
    rm -rf graspnetAPI models
    mkdir graspnetAPI models
    cd ~/graspnet-baseline
    mv dataset knn models pointnet2 utils ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/
    cd ~
    mv graspnetAPI ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet
    cp -r graspnetAPI/graspnetAPI/* graspnet/graspnetAPI
    cp graspnetAPI/copy_rect_labels.py graspnetAPI/gen_pickle_dexmodel.py graspnet/graspnetAPI
    
    cp models/backbone.py models/graspnet.py models/loss.py models/modules.py graspnet/models
    cp knn/knn_modules.py graspnet/models
    cp pointnet2/pointnet2_modules.py pointnet2/pointnet2_utils.py pointnet2/pytorch_utils.py pointnet2/setup.py graspnet/models
    cp utils/collision_detector.py utils/data_utils.py utils/label_generation.py utils/loss_utils graspnet/models
    cp dataset/graspnet_dataset.py graspnet/models
    touch ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/graspnet/models/__init__.py
    
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws/src/graspnet/graspnet/models
    sed -i 's/def pred_decode(end_points):/def pred_decode(end_points, gripper_max_width):/' graspnet.py
    sed -i 's/GRASP_MAX_WIDTH/gripper_max_width/I' graspnet.py
    sudo sed -i 's/grasp_width = 1.2 \* end_points\['\''grasp_width_pred'\''\]\[i\]/grasp_width = 1.8 \* end_points\['\''grasp_width_pred'\''\]\[i\]/' graspnet.py

    ```


8. Colcon build - Re-run if any packages timeout during compile

    ```shell
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws
    export MAKEFLAGS="-j3"
    colcon build --mixin release
    ```
 
9. NOTE: If you are running on our setup, remember to set your IP to 172.31.1.148 and Netmask to 255.255.255.0, also ensure that you are correctly connected to the setup (2 USB's 1 Ethernet). ([Static IP configuration](https://linuxconfig.org/how-to-configure-static-ip-address-on-ubuntu-22-04-jammy-jellyfish-desktop-server))
   
10. Running the system

    ```shell
    cd ~/Dual_Kuka_LLM_Bachelor/p6_ws
    source install/setup.bash
    ros2 launch robutler_bringup robutler.launch.py
    ```
    
11. Recommendations - *Don't do this, if you run multiple ROS Distros*

    ```shell
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
    echo "source ~/Dual_Kuka_LLM_Bachelor/p6_ws/install/setup.bash" >> ~/.bashrc
    ```

## Contributors
This project was developed by group 660 at Aalborg University, during their Robotics Bachelor. Every member of the group can be found listed below, alongside their GitHub pages:

<section id="sec_contributors">
<table>
  <tr> 
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/Gustav-Bay"><img src="https://avatars.githubusercontent.com/u/120191982?v=4" width="100px;" alt=""/><br/><sub><b>Gustav Bay Baastrup</b></sub></a></br><a href="gttps://github.com/Gustav-Bay" title="">🤖</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/thor2643"><img src="https://avatars.githubusercontent.com/u/66319719?v=4" width="100px;" alt=""/><br/><sub><b>Thor Iversen</b></sub></a></br><a href="gttps://github.com/thor2643" title="">👨‍🌾</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/xdKazer"><img src="https://avatars.githubusercontent.com/u/116707938?v=4" width="100px;" alt=""/><br/><sub><b>Kasper Lauritsen</b></sub></a></br><a href="gttps://github.com/xdKazer" title="">🎥</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/silasjensen2001"><img src="https://avatars.githubusercontent.com/u/54105795?v=4" width="100px;" alt=""/><br/><sub><b>Silas Jensen</b></sub></a></br><a href="gttps://github.com/silasjensen2001" title="">😎</a></td>
    <td align="center"><a target="_blank" rel="noreferrer noopener" href="https://github.com/signeskuldbol"><img src="https://avatars.githubusercontent.com/u/117270262?v=4" width="100px;" alt=""/><br/><sub><b>Signe Møller-Skuldbøl</b></sub></a></br><a href="gttps://github.com/signeskuldbol" title="">🌸</a></td>
  </tr>
</table>

