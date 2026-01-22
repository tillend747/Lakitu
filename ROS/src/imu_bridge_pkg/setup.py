from setuptools import find_packages, setup

package_name = 'imu_bridge_pkg'

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
    maintainer='till-kappeler',
    maintainer_email='tillend747@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
  entry_points={
    'console_scripts': [
        'imu_serial_bridge = imu_bridge_pkg.imu_serial_node:main',
        'imu_odometry_node = imu_bridge_pkg.imu_odometry_node:main',
    ],
},
)
