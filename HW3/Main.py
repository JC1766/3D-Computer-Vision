
import numpy as np
import sys
import cv2
from PIL import Image
import pickle
import time
from scipy.signal import medfilt
from scipy.ndimage.filters import maximum_filter as maxfilt

P = np.array([[776.649963,-298.408539,-32.048386,993.1581875,132.852554,120.885834,-759.210876,1982.174000,0.744869,0.662592,-0.078377,4.629312012],
    [431.503540,586.251892,-137.094040,1982.053375,23.799522,1.964373,-657.832764,1725.253500,-0.321776,0.869462,-0.374826,5.538025391],
    [-153.607925,722.067139,-127.204468,2182.4950,141.564346,74.195686,-637.070984,1551.185125,-0.769772,0.354474,-0.530847,4.737782227],
    [-823.909119,55.557896,-82.577644,2498.20825,-31.429972,42.725830,-777.534546,2083.363250,-0.484634,-0.807611,-0.335998,4.934550781],
    [-715.434998,-351.073730,-147.460815,1978.534875,29.429260,-2.156084,-779.121704,2028.892750,0.030776,-0.941587,-0.335361,4.141203125],
    [-417.221649,-700.318726,-27.361042,1599.565000,111.925537,-169.101776,-752.020142,1982.983750,0.542421,-0.837170,-0.070180,3.929336426],
    [94.934860,-668.213623,-331.895508,769.8633125,-549.403137,-58.174614,-342.555359,1286.971000,0.196630,-0.136065,-0.970991,3.574729736],
    [452.159027,-658.943909,-279.703522,883.495000,-262.442566,1.231108,-751.532349,1884.149625,0.776201,0.215114,-0.592653,4.235517090]])

c_dict = {}
s_dict = {}
for i in range(8):
    c_dict[i] = Image.open("cam0" + str(i) + "_00023_0000008550.png")
    s_dict[i] = Image.open("silh_cam0" + str(i) + "_00023_0000008550.pbm")

print(c_dict[0].size,s_dict[1].size)
# height, width, rgb values, image number
c_mat = np.zeros((582,780,3,8))
s_mat = np.zeros((582,780,8))
p_mat = np.zeros((3,4,8))
for i in range(8):
    c_mat[:,:,:,i] = c_dict[i]
    s_mat[:,:,i] = s_dict[i]
    p_mat[:,:,i] = np.reshape(P[i],(3,4))
print(s_mat[:,:,0].shape,s_mat[:,:,1])
x_range = 5
y_range = 6
z_range = 2.5
volume = x_range*y_range*z_range
vox_num = 1000
vox_size = np.power((volume/vox_num),1/3)
vox_grid = []
flag = 0
vox_mat = []
color_mat = []


for x in np.arange(-2.5, 2.5, vox_size):
    for y in np.arange(-3, 3, vox_size):
        for z in np.arange(0, 2.5, vox_size):
            pass_mat = np.zeros(8)
            coord = [[x, y, z, 1]]
            for i in range(8):
                point = np.dot(p_mat[:,:,i],np.transpose(coord))
                point = point/point[2]
                # print(point)
                # check if point is within bounds
                if((0<=point[1]<582) and (0<=point[0]<780)):
                    pass_mat[i] = s_mat[int(point[1]),int(point[0]),i]
            # if point is in the silhouette for all 8 views, mark as occupied
            if(np.sum(pass_mat) == 8):
                vox_grid.append([x,y,z])


                r = (c_mat[int(point[1]),int(point[0]),0,7])
                g = (c_mat[int(point[1]), int(point[0]), 1, 7])
                b = (c_mat[int(point[1]), int(point[0]), 2, 7])
                color_mat.append([r,g,b])

            if(flag == 0):
                vox_mat.append([x,y,z])
                flag+=1
                p_vec = [x,y,z]
                continue
            if(p_vec[0]==x and p_vec[1] ==y):
                flag+=1




print(vox_grid)
print(color_mat)
print(vox_mat)
print(p_vec)