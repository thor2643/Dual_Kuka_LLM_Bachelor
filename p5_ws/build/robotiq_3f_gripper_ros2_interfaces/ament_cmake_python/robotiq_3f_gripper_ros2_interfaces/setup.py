from setuptools import find_packages
from setuptools import setup

setup(
    name='robotiq_3f_gripper_ros2_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('robotiq_3f_gripper_ros2_interfaces', 'robotiq_3f_gripper_ros2_interfaces.*')),
)
