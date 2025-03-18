from setuptools import find_packages, setup

package_name = 'sim_camera_capture'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='xdkazer',
    maintainer_email='kkl@stofanet.dk',
    description='Simple script for performing a screen capture with opencv, which is subsequently published to a ros2 topic',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'image_service = sim_camera_capture.imgcapturesrv:main',
        	'image_client = sim_camera_capture.imgcapturecli:main',
        ],
    },
)
