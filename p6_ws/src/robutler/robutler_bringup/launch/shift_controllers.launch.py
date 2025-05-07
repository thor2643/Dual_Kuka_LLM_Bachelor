import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro
from launch.actions import ExecuteProcess
import subprocess
import time
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource


urdf_path = os.path.join(
    get_package_share_directory('lbr_description'),
    'urdf',
    'dual_arm',
    'dual_arm.xacro'
)

controller_path = os.path.join(
    get_package_share_directory('dual_arm_moveit_config'),
    'config',
    'ros2_controllers.yaml',
)


# Kill any existing robot_state_publisher nodes
try:
    subprocess.run("gnome-terminal -- bash -c 'pkill -f ros2_control_no; exec bash'", check=True, shell=True)
    print("Successfully killed ros2_control_node processes.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while killing ros2_control_node processes: {e}")

time.sleep(1)

# Kill any existing ros2_control_node processes
try:
    subprocess.run("gnome-terminal -- bash -c 'pkill -f robot_state_pub; exec bash'", check=True, shell=True)
    print("Successfully killed robot_state_publisher processes.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while killing ros2_control_node processes: {e}")


controller_names = ["right_arm_controller", "left_arm_controller", "joint_state_broadcaster", "threef_gripper_controller", "twof_gripper_controller"]

# Process the xacro file to generate the URDF
def generate_robot_description():
    doc = xacro.process_file(urdf_path)
    return doc.toxml()

def generate_launch_description():
    """Launch file for robot state publisher (rsp) with Isaac simulation plugin"""

    ld = LaunchDescription()
    
    # Given the published joint states, publish tf for the robot links and the robot description
    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        respawn=False,
        output="screen",
        parameters=[
            {"robot_description": generate_robot_description()},
        ],
    )
    ld.add_action(rsp_node)

    # Load the controllers
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": generate_robot_description()},
            controller_path,
        ],
    )

    ld.add_action(ros2_control_node)

    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('dual_arm_moveit_config'),
                    'launch',
                    'spawn_controllers.launch.py',
                )
            ),
        )
    )
        
    return ld