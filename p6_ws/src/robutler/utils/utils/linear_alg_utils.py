import numpy as np
from scipy.spatial.transform import Rotation as R

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
