from launch_ros.actions import Node
from launch import LaunchDescription
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_spawn_controllers_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("mock_dual_arm", package_name="mock_dual_arm_moveit_config").to_moveit_configs()
    return generate_spawn_controllers_launch(moveit_config)
