"""
Run from the ~/openvslam/example folder

python3 csv2ply.py
"""
import pandas as pd
from pyntcloud import PyntCloud
import csv
import open3d as o3d
import numpy as np
print('All imports successful')

# After prior conversion from msg format to csv file format,
# Convert from csv file format to txt format
csv_file ="output_file.csv"
txt_file = "output_file.txt"
with open(txt_file, "w") as my_output_file:
    with open(csv_file, "r") as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()

# Note there are only three columns here, x, y and z
cloud = PyntCloud.from_file("output_file.txt",
                            sep=" ",
                            header=0,
                            names=["x","y","z"])

# Use open3d to convert txt file to ply file format
ply = o3d.io.read_point_cloud("output_file.txt", format='xyz')
print(ply)
o3d.io.write_point_cloud("output_file.ply", ply)

print("Load a ply point cloud, print it, and render it")
ply = o3d.io.read_point_cloud("output_file.ply")
print(ply)
print(np.asarray(ply.points))

# Visualize the cloud points
o3d.visualization.draw_geometries([ply],
                                  zoom=0.05,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])
