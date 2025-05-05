from setuptools import setup
import os
from glob import glob

package_name = 'isaac_cam_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=['isaac_cam_pkg'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
        (os.path.join('share', package_name, 'srv'), glob('srv/*.srv')),
    ],
    install_requires=['setuptools', 'project_interfaces'],
    zip_safe=True,
    maintainer='silas',
    maintainer_email='silasjensen2001@gmail.com',
    description='Package for interfacing Isaac Sim with ROS2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_subscriber = isaac_cam_pkg.camera_subscriber:main',
            'isaac_cam_bridge = isaac_cam_pkg.isaac_cam_bridge:main',
            'isaac_cam_client = isaac_cam_pkg.isaac_cam_client:main',
            'spawn_cube_service = isaac_cam_pkg.spawn_cube_service:main',
        ],
    },
)
