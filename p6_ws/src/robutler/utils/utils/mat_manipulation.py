import math
import numpy as np

def convert_to_transformation_matrix(rotation, translation):
    """
    Converts a rotation matrix and translation vector into a 4x4 transformation matrix.
    """
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = np.array(rotation)
    transformation_matrix[:3, 3] = np.array(translation).flatten()
    return transformation_matrix

# Combine multiple transformations by averaging the rotation and translation components
def average_transformations(*matrices):
    """
    Averages multiple 4x4 transformation matrices by averaging their rotation and translation components.
    """
    if len(matrices) == 0:
        raise ValueError("At least one transformation matrix is required.")

    # Initialize accumulators for rotation and translation
    R_sum = np.zeros((3, 3))
    t_sum = np.zeros(3)

    # Sum up the rotation matrices and translation vectors
    for T in matrices:
        R_sum += T[:3, :3]
        t_sum += T[:3, 3]

    # Average the rotation matrices and re-orthogonalize using SVD
    R_avg = R_sum / len(matrices)
    U, _, Vt = np.linalg.svd(R_avg)
    R_avg = np.dot(U, Vt)

    # Average the translation vectors
    t_avg = t_sum / len(matrices)

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