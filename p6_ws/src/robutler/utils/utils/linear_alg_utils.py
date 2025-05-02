import numpy as np
from scipy.spatial.transform import Rotation as R
import math

def build_transform_matrix_from_rpy(x, y, z, roll, pitch, yaw):
    """
    Constructs a 4x4 homogeneous transformation matrix from translation and RPY rotation (in degrees).

    Args:
        x, y, z (float): Translation in meters
        roll, pitch, yaw (float): Rotation in degrees

    Returns:
        np.ndarray: 4x4 transformation matrix
    """
    T = np.eye(4)

    # Translation
    T[0, 3] = x
    T[1, 3] = y
    T[2, 3] = z

    # Rotation
    r = R.from_euler('xyz', [roll, pitch, yaw], degrees=True)
    T[:3, :3] = r.as_matrix()

    return T

def T_mat_from_Rotm_tvec(rotation, translation):
    """
    Converts a rotation matrix and translation vector into a 4x4 transformation matrix.
    """
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = np.array(rotation)
    transformation_matrix[:3, 3] = np.array(translation).flatten()

    return transformation_matrix

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

def euler_to_quat(euler_angles):
    cr = np.cos(np.deg2rad(euler_angles[0]) * 0.5)
    sr = np.sin(np.deg2rad(euler_angles[0]) * 0.5)
    cp = np.cos(np.deg2rad(euler_angles[1]) * 0.5)
    sp = np.sin(np.deg2rad(euler_angles[1]) * 0.5)
    cy = np.cos(np.deg2rad(euler_angles[2]) * 0.5)
    sy = np.sin(np.deg2rad(euler_angles[2]) * 0.5)

    q_w = cr * cp * cy + sr * sp * sy
    q_x = sr * cp * cy - cr * sp * sy
    q_y = cr * sp * cy + sr * cp * sy
    q_z = cr * cp * sy - sr * sp * cy

    return [q_w, q_x, q_y, q_z]

def quat_to_euler(w, x, y, z):
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

def get_zyz_transform(): 
    """
    Returns a transformation matrix that rotates the Z axis by 90 degrees, then the Y axis by 90 degrees, and finally the Z axis by 90 degrees. Used to align the camera frame with the gripper frame when simulating with Isaac Sim.
    """
    theta_z = np.deg2rad(90)
    Rz = np.array([
        [np.cos(theta_z), -np.sin(theta_z), 0],
        [np.sin(theta_z),  np.cos(theta_z), 0],
        [0,               0,                1]
    ])
    theta_y = np.deg2rad(90)
    Ry = np.array([
        [ np.cos(theta_y), 0, np.sin(theta_y)],
        [ 0,               1, 0              ],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])
    Rotation = Rz @ Ry @ Rz
    T_rotation = np.eye(4)
    T_rotation[:3, :3] = Rotation
    
    return T_rotation

def flip_if_near_180(angle_deg):
    """
    If angle is near ±180, flip it to the equivalent small negative or positive.
    Assumes input is already in [-180, 180)
    """
    if angle_deg > 90:
        return angle_deg - 180
    elif angle_deg < -90:
        return angle_deg + 180
    return angle_deg
