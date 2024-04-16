import numpy as np
from scipy.spatial.transform import Rotation as R
def fix_vive_pose_matrix(pose_matrix):
    if pose_matrix is None:
        return None
    else:
        OPENXR_TO_RHS = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

        pose_matrix = np.array(
            [
                list(pose_matrix[0]),
                list(pose_matrix[1]),
                list(pose_matrix[2]),
                [0, 0, 0, 1]
            ]
        )

        pose_matrix[:3, 3:4] = OPENXR_TO_RHS @ pose_matrix[:3, 3:4]
        # pose_matrix[:3, 3:4] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]]) @ pose_matrix[:3, 3:4]
        pose_matrix[:3, :3] = OPENXR_TO_RHS @ np.linalg.inv(np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]) @ pose_matrix[:3, :3])

        return np.concatenate([pose_matrix[:3, 3], R.from_matrix(pose_matrix[:3, :3]).as_quat()])