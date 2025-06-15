from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, get_package_prefix
import os
from launch.actions import ExecuteProcess
def generate_launch_description():
    # Get the path to the package and the URDF file
    pkg_description = get_package_share_directory('oakd_description')
    urdf_file = os.path.join(pkg_description, "urdf", 'oakd.urdf')

    mesh_pkg_share_dir = os.pathsep + os.path.join(get_package_prefix('oakd_description'), 'share')
    #mesh_pkg_gripper_share_dir = os.pathsep + os.path.join(get_package_prefix('robotiq_85_description'), 'share')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] += mesh_pkg_share_dir
        #os.environ['GAZEBO_MODEL_PATH'] += mesh_pkg_gripper_share_dir
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  mesh_pkg_share_dir
        #os.environ['GAZEBO_MODEL_PATH'] =  mesh_pkg_gripper_share_dir

    # Read the URDF file
    with open(urdf_file, 'r') as file:
        urdf_content = file.read() 
    
    # Return the LaunchDescription
    return LaunchDescription([
        Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{'robot_description': urdf_content}]),
        ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
        output='screen'),
        Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='robot_spawner',
        output='screen',
        arguments=["-topic", "/robot_description", "-entity", "oakd"]),
    ])

if __name__ == '__main__':
    generate_launch_description()