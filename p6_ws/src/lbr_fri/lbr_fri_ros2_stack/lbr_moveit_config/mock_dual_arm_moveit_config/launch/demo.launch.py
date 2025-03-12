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
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    package_path_xacro = get_package_share_directory('lbr_description')
    package_path_cont = get_package_share_directory('mock_dual_arm_moveit_config')
    
    xacro_file = os.path.join(package_path_xacro, 'urdf', 'mock_dual_arm', 'mock_dual_arm.xacro')
    controllers_yaml = os.path.join(package_path_cont, 'config', 'ros2_controllers.yaml')
    
    # Process the xacro file
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    
    # Gazebo Stuff - Needed for camera simulation
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])]
        )
    )

    # Generate the robot description XML
    robot_description = {'robot_description': doc.toxml()}
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )
    
    robot_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic','robot_description',
                   '-entity','robot'],
        output='screen'
    )
    
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )
    
    load_joint_trajectory_controller_right = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'right_arm_controller'],
        output='screen'
    )
    
    load_joint_trajectory_controller_left = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'left_arm_controller'],
        output='screen'
    )
    
    load_joint_position_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'forward_position_controller'],
        output='screen'
    )
    
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='screen',
        parameters=[robot_description, controllers_yaml, {'use_sim_time': True}],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')]
    )
    
    # Camera publisher node to be triggered after Gazebo starts
    node_camera_publisher = Node(
        package='image_tools',
        executable='cam2image',
        name='camera_publisher',
        output='screen',
        remappings=[('/image', '/camera/image_raw')]
    )
    
    moveit_config = MoveItConfigsBuilder("mock_dual_arm", package_name="mock_dual_arm_moveit_config").to_moveit_configs()

    # Register event handler to trigger camera publisher after Gazebo is launched
    event_handler = RegisterEventHandler(
        OnProcessExit(
            target_action=robot_spawn_node,  # Trigger after the Gazebo launch finishes
            on_exit=[node_camera_publisher]
        )
    )

    return LaunchDescription([
        generate_demo_launch(moveit_config),  # MoveIt launch
        gazebo_launch,  # Launch Gazebo with ExecuteProcess
        robot_spawn_node,  # Spawn robot in Gazebo
        event_handler,  # Event handler to launch the camera publisher after Gazebo starts
    ])

