from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('gpd_ros2')
    config_path = os.path.join(pkg_share, 'config', 'grasp_cfg.cfg')
    
    return LaunchDescription([
        Node(
            package='gpd_ros2',
            executable='gpd_node',
            name='gpd_node',
            output='screen',
            parameters=[
                {'config_path': config_path}
            ],
            cwd=pkg_share
        )
    ])
