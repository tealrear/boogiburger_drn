from setuptools import find_packages, setup

package_name = 'camera_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/camera.launch.py']),
        ('share/camera_test/models', ['models/best.pt']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bird99',
    maintainer_email='bird99@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
          'detect_human=camera_test.detect_human:main',
          'detect_object=camera_test.detect_object:main',
          'visualize=camera_test.visualize:main',
          'qt_camera=camera_test.qt_camera_gui:main',
          'camera_ui=camera_test.camera_ui:main',
        ],
    },
)
