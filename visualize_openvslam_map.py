"""
Please Modify the path to .msg file. 

usage; 

Run from the ~/openvslam/example folder

python3 visualize_openvslam_map.py ~/openvslam/build/map.msg
"""

import msgpack
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy.linalg import inv
from scipy.spatial.transform import Rotation as R
import open3d as o3d
import sys

if len(sys.argv) < 2:
    print(
        "ERROR: Please provide path to .msg file. Example usage is; python3 visualize_openvslam_map.py path_to.msg"
    )
    exit()

with open(sys.argv[1], "rb") as f:
    upacked_msg = msgpack.Unpacker(f)
    packed_msg = upacked_msg.unpack()

print(packed_msg.keys())

keyframes = packed_msg[b'keyframes']
landmarks = packed_msg[b'landmarks']

# FILL IN KEYFRAME POINTS(ODOMETRY) TO ARRAY
keyframe_points = []
keyframe_points_color = []
for keyframe in keyframes.values():
    # get conversion from camera to world
    trans_cw = np.matrix(keyframe[b'trans_cw']).T
    rot_cw = R.from_quat(keyframe[b'rot_cw']).as_matrix()
    # compute conversion from world to camera
    rot_wc = rot_cw.T
    trans_wc = -rot_wc * trans_cw
    keyframe_points.append((trans_wc[0, 0], trans_wc[1, 0], trans_wc[2, 0]))

keyframe_points = np.array(keyframe_points)
keyframe_points_color = np.repeat(np.array([[0., 1., 0.]]),
                                  keyframe_points.shape[0],
                                  axis=0)

# FILL IN LANDMARK POINTS TO ARRAY
landmark_points = []
landmark_points_color = []
for lm in landmarks.values():
    print(lm.keys())
    landmark_points.append(lm[b'pos_w'])
    landmark_points_color.append([
        abs(lm[b'pos_w'][1]) * 4,
        abs(lm[b'pos_w'][1]) * 2,
        abs(lm[b'pos_w'][1]) * 3
    ])

landmark_points = np.array(landmark_points)
landmark_points_color = np.array(landmark_points_color)

# CONSTRUCT KEYFRAME(ODOMETRY) FOR VISUALIZTION
keyframe_points_pointcloud = o3d.geometry.PointCloud()
keyframe_points_pointcloud.points = o3d.utility.Vector3dVector(keyframe_points)
keyframe_points_pointcloud.colors = o3d.utility.Vector3dVector(
    keyframe_points_color)

# CONSTRUCT LANDMARK POINTCLOUD FOR VISUALIZTION
landmark_points_pointcloud = o3d.geometry.PointCloud()
landmark_points_pointcloud.points = o3d.utility.Vector3dVector(landmark_points)
landmark_points_pointcloud.colors = o3d.utility.Vector3dVector(
    landmark_points_color)

# VISULIZE MAP
o3d.visualization.draw_geometries([
    keyframe_points_pointcloud, landmark_points_pointcloud,
    o3d.geometry.TriangleMesh.create_coordinate_frame()
])