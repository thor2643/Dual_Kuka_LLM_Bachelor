import numpy as np
import tf2_ros
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
import math
import os
from scipy.spatial.transform import Rotation 

# Calibrated transformation matrix from world to moveit coordinates based on left arm
T_world_moveit = np.array([ [ 0.99993911, -0.01089373,  0.00176324, -0.02348162],
                            [ 0.01089142,  0.99993982,  0.00131455, -0.03821792],
                            [-0.00177746, -0.00129526,  0.99999758,  0.80140745],
                            [ 0.0,         0.0,         0.0,         1.0       ] ])

trasnform = {"DANIILIDIS": {
        "depth": {
            "R_cam2gripper": [
                [
                    -0.10104078926288541,
                    -0.9947340176622806,
                    0.017175360566569656
                ],
                [
                    -0.9947541970636232,
                    0.10073571066061836,
                    -0.01778774921139175
                ],
                [
                    0.015963907085691006,
                    -0.018882550229205486,
                    -0.9996942547436206
                ]
            ],
            "t_cam2gripper": [
                [
                    0.09402568876136451
                ],
                [
                    0.02717960285044562
                ],
                [
                    0.1578761903166473
                ]
            ]
        },
    },
    "PARK": {
        "depth": {
            "R_cam2gripper": [
                [
                    -0.08239743142594505,
                    -0.9963432571467553,
                    0.022600381249022077
                ],
                [
                    -0.9963163659903803,
                    0.0818122625150218,
                    -0.02569927162189075
                ],
                [
                    0.023756307670369237,
                    -0.024634683687184286,
                    -0.9994142135298573
                ]
            ],
            "t_cam2gripper": [
                [
                    0.09090569068801656
                ],
                [
                    0.027666959247674087
                ],
                [
                    0.1683650133548136
                ]
            ]
        },
    }
}

def convert_to_transformation_matrix(rotation, translation):
    """
    Converts a rotation matrix and translation vector into a 4x4 transformation matrix.
    """
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = np.array(rotation)
    transformation_matrix[:3, 3] = np.array(translation).flatten()
    return transformation_matrix

# Combine the two transformations by averaging the rotation and translation components
def average_transformations(T1, T2):
    """
    Averages two 4x4 transformation matrices by averaging their rotation and translation components.
    """
    R1, t1 = T1[:3, :3], T1[:3, 3]
    R2, t2 = T2[:3, :3], T2[:3, 3]

    # Average the rotation matrices and re-orthogonalize using SVD
    R_avg = (R1 + R2) / 2
    U, _, Vt = np.linalg.svd(R_avg)
    R_avg = np.dot(U, Vt)

    # Average the translation vectors
    t_avg = (t1 + t2) / 2

    # Construct the averaged transformation matrix
    T_avg = np.eye(4)
    T_avg[:3, :3] = R_avg
    T_avg[:3, 3] = t_avg

    return T_avg

def quaternion_to_euler_angle( w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z

def invert_transformation_matrix(T):
            """
            Inverts a 4x4 transformation matrix.
            """
            R = T[:3, :3]
            t = T[:3, 3]
            R_inv = R.T
            t_inv = -np.dot(R_inv, t)
            T_inv = np.eye(4)
            T_inv[:3, :3] = R_inv
            T_inv[:3, 3] = t_inv
            return T_inv

t_matrices = []

# Convert and print transformation matrices for DANIILIDIS and PARK
for key, value in trasnform.items():
    for depth_key, depth_value in value.items():
        R = depth_value["R_cam2gripper"]
        t = depth_value["t_cam2gripper"]
        T = convert_to_transformation_matrix(R, t)
        t_matrices.append(T)
        #print(f"Transformation matrix for {key} ({depth_key}):\n{T}\n")

# Compute the averaged transformation matrix
T_combined = average_transformations(t_matrices[0], t_matrices[1])
#print(f"Combined Transformation Matrix from cam to gripper:\n{T_combined}\n")

t_matrices.append(T_combined)

# Transform a test position from camera coordinates to gripper coordinates
center_pts = [[0.25, 0.65, 0.3, 1]]  # Example center points in camera coordinates

center_pts_world = np.dot(t_matrices[0], np.array(center_pts).T).T
#print(f"Transformed center points in gripper coordinates (DANIILIDIS):\n{center_pts_world}\n")

center_pts_world = np.dot(t_matrices[1], np.array(center_pts).T).T
#print(f"Transformed center points in gripper coordinates (PARK):\n{center_pts_world}\n")

# Transform the center points using the combined transformation matrix
center_pts_world = np.dot(t_matrices[2], np.array(center_pts).T).T
#print(f"Transformed center points in gripper coordinates (Combined):\n{center_pts_world}\n")

rclpy.init()  # Initialize the ROS client library
node = Node("camera2world_tf_node")

# Notation T_"from"_"to" transformation matrix from "from_frame" to "to_frame"
T_cam_gripper = T_combined

print(f"Transformation Matrix from Camera to Gripper:\n{T_cam_gripper}\n")

tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer, node)

# Get gripper pose (try a few times if not successful)
for i in range(5):
    try:
        rclpy.spin_once(node, timeout_sec=0.1)

        transform_3: TransformStamped = tf_buffer.lookup_transform(
            "world", "2f_tool0", rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=2.0))

        # Assuming transform_3 is your TransformStamped object
        quaternion = [
            transform_3.transform.rotation.w,
            transform_3.transform.rotation.x,
            transform_3.transform.rotation.y,
            transform_3.transform.rotation.z,
        ]

        # Convert quaternion to Euler angles
        roll, pitch, yaw = quaternion_to_euler_angle(*quaternion)

        t_gripper_moveit =  [
            transform_3.transform.translation.x,
            transform_3.transform.translation.y,
            transform_3.transform.translation.z
        ]

        R_gripper_moveit = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=True).as_matrix()
        T_gripper_moveit = convert_to_transformation_matrix(R_gripper_moveit, t_gripper_moveit)

        # Invert to get from gripper to MoveIt
        #T_gripper_moveit = invert_transformation_matrix(T_gripper_moveit)
        print(f"Inverted Transformation Matrix (Gripper to MoveIt):\n{T_gripper_moveit}\n")

        break

    except tf2_ros.LookupException:
        if i < 4:
            node.get_logger().info("Retrying...")
            rclpy.spin_once(node, timeout_sec=0.1)
        else:
            node.get_logger().error("Failed to get gripper pose after multiple attempts")

T_moveit_world = invert_transformation_matrix(T_world_moveit)
print(f"Transformation Matrix from MoveIt to World:\n{T_moveit_world}\n")

#T_cam_world = T_cam_gripper  @ T_gripper_moveit @ T_moveit_world
T_cam_world = T_moveit_world @ T_gripper_moveit @ T_cam_gripper 

print(f"Transformation Matrix from Camera to World:\n{T_cam_world}\n")

# Invert to get from world to camera
T_world_cam = invert_transformation_matrix(T_cam_world)

print(f"Inverted Transformation Matrix (World to Camera):\n{T_world_cam}\n")