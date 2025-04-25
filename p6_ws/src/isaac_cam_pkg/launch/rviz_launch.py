from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_pub_sim_camera',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'sim_camera'],
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', '/home/silas/Desktop/test_point_cloud_ws/src/isaac_cam_pkg/config/rviz_pointcloud_config.rviz'],
            output='screen'
        ),
    ])
