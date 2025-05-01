import numpy as np
import tf2_ros
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from scipy.spatial.transform import Rotation 
from utils.mat_manipulation import (
    convert_to_transformation_matrix,
    quaternion_to_euler_angle,
    invert_transformation_matrix,
)

# Get transform between two links defined in the loaded urdf
ref_link = "world"
end_link = "2f_tool0"

rclpy.init()  # Initialize the ROS client library
node = Node("get_pose_node")

tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer, node)

# Get gripper pose (try a few times if not successful)
for i in range(5):
    try:
        rclpy.spin_once(node, timeout_sec=0.1)

        transform_3: TransformStamped = tf_buffer.lookup_transform(
            ref_link, end_link, rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=2.0))

        # Assuming transform_3 is your TransformStamped object
        quaternion = [
            transform_3.transform.rotation.w,
            transform_3.transform.rotation.x,
            transform_3.transform.rotation.y,
            transform_3.transform.rotation.z,
        ]

        # Convert quaternion to Euler angles
        roll, pitch, yaw = quaternion_to_euler_angle(*quaternion)

        t_vec =  [
            transform_3.transform.translation.x,
            transform_3.transform.translation.y,
            transform_3.transform.translation.z
        ]

        R_mat = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=True).as_matrix()
        T_mat = convert_to_transformation_matrix(R_mat, t_vec)

        T_moveit_world = np.array([
            [0.99993911, 0.01089142, -0.00177746, 0.02532091],
            [-0.01089373, 0.99993982, -0.00129526, 0.03899785],
            [0.00176324, 0.00131455, 0.99999758, -0.80131387],
            [0., 0., 0., 1.]
        ])

        T_mat_world = T_moveit_world @ T_mat

        print(f"Transform from {ref_link} to {end_link} in world frame:")
        print(f"Transformation matrix:\n{T_mat_world}\n")

        R_euler = Rotation.from_matrix(T_mat_world[:3, :3]).as_euler("xyz", degrees=True)
        print(f"Roll: {R_euler[0]}, Pitch: {R_euler[1]}, Yaw: {R_euler[2]}")
        print(f"Translation: x={T_mat_world[0, 3]}, y={T_mat_world[1, 3]}, z={T_mat_world[2, 3]}\n")





        break

    except tf2_ros.LookupException:
        if i < 4:
            node.get_logger().info("Retrying...")
            rclpy.spin_once(node, timeout_sec=0.1)
        else:
            node.get_logger().error("Failed to get gripper pose after multiple attempts.\n" \
            "Please check if the robot is running and the TF tree is correct.")