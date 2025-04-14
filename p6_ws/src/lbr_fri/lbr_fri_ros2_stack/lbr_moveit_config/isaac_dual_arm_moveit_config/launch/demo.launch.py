import os
import xacro

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch


from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_path_xacro = get_package_share_directory('lbr_description')
    package_path_cont = get_package_share_directory('isaac_dual_arm_moveit_config')
    
    xacro_file = os.path.join(package_path_xacro, 'urdf', 'isaac_dual_arm', 'isaac_dual_arm.xacro')
    
    #controllers_yaml = os.path.join(package_path_cont, 'config', 'ros2_controllers.yaml')
    
    # Process the xacro file
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    # Generate the robot description XML
    robot_description = {'robot_description': doc.toxml()}
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )
    
    moveit_config = MoveItConfigsBuilder("isaac_dual_arm", package_name="isaac_dual_arm_moveit_config").to_moveit_configs()
        
    return generate_demo_launch(moveit_config)
    
    
    
    


