import numpy as np
import glob
import cv2

img_array = []
count = 0

filenames = [img for img in glob.glob('/home/govind/openvslam/example/kitti/dataset/sequences/00/image_0/*.png')]
filenames.sort()

for filename in filenames:
    
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    print ('Frame ',count,' processed.')
    count+=1
 
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('kitti_video.mp4',fourcc, 20.0, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()