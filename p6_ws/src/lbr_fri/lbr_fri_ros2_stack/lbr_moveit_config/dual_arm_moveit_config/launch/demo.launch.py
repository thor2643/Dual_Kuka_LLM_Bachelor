from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Specify the path to the new URDF/Xacro file
    urdf_path = os.path.join(
        get_package_share_directory('lbr_description'),
        'urdf',
        'dual_arm',
        'dual_arm_sim.xacro' # Change back to 'dual_arm_sim.urdf' after test
    )

    # Build the MoveIt configuration with the new URDF file
    moveit_config = (
        MoveItConfigsBuilder("dual_arm", package_name="dual_arm_moveit_config")
        .robot_description(file_path=urdf_path)
        .to_moveit_configs()
    )

    return generate_demo_launch(moveit_config)
