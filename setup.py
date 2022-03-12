from setuptools import setup

package_name = 'strategy'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yclin_lab',
    maintainer_email='ianlin79928@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'strategy_node = strategy.strategy_node:main',
            'imu_node = strategy.imu_node:main'
        ],
    },
)
