from types import new_class
import numpy as np
import sys
import cv2
from PIL import Image

def normalize(width,height):
    normMat = np.array([[width+height,0,width/2],[0,width+height,height/2],[0,0,1]])
    Tn = np.linalg.inv(normMat)
    # print(Tn)
    return Tn


def computeA(source, target):
    [a,b,c] = source
    [x,y,z] = target
    matrixA = np.array([[0,0,0,-a,-b,-c,y*a,y*b,y*c],[a,b,c,0,0,0,-x*a,-x*b,-x*c]])
    return matrixA

def imageWarp(original, new, H):
    (h,w,_) = new.shape
    for i in range(0,w):
        for j in range(0,h):
            coord = [i,j,1]
            # getting the warped coordinates
            res = np.matmul(H, coord)
            # print(res)
            # converting homogeneous coordinates back to regular inhomogeneous coords
            x = res[0]/res[2]
            y = res[1]/res[2]
            # split the coords to get values before and after the decimal for color sampling
            xsplit = str(x).split('.')
            ysplit = str(y).split('.')
            i_whole = int(ysplit[0])
            j_whole = int(xsplit[0])
            i_dec = float('0.'+ysplit[1])
            j_dec = float('0.'+xsplit[1])

            # if the warped point is close enough to actual point just sample the point,
            # otherwise use binlinear interpolation to get the rgb values
            if(i_dec+j_dec <= 0.01):
                new[j][i] = original[i_whole][j_whole]
            else:
                rgb = [0,0,0]
                for k in range(0,3):
                    res = (1-i_dec)*(1-j_dec)*original[i_whole][j_whole][k] + (i_dec)*(1-j_dec)*original[i_whole+1][j_whole][k] \
                    + (i_dec)*(j_dec)*original[i_whole+1][j_whole-1][k] + (1-i_dec)*(j_dec)*original[i_whole][j_whole-1][k]
                    rgb[k] = int(res)
                new[j][i] = rgb
    newImg = Image.fromarray(new)
    return newImg


def main():
    image = Image.open("basketball-court.ppm")
    # image.show()
    # print(image.size)
    newImg = Image.new(mode = "RGB", size = (940, 500))
    # newImg.show()
    # [23,193] -> [0,0] 
    # [247,51] -> [939,0] 
    # [402,74] -> [939,499] 
    # [279,279] -> [0,499]
    arr1 = [[23,193,1],[247,51,1],[402,74,1],[279,279,1]]
    arr2 = [[0,0,1],[939,0,1],[939,499,1],[0,499,1]]
    T1 = normalize(488,366)
    T2 = normalize(940,500)

    # normalize arr2 and arr2
    for i in range(0,4):
        # print(arr1[i])
        arr1[i] = np.matmul(T1,arr1[i])
        arr2[i] = np.matmul(T2,arr2[i])
    # print(arr1)
    # print(arr2)

    # compute A matrix
    A = np.zeros((8,9))
    for i in range(0,4):
        Ai = computeA(arr1[i],arr2[i])
        it = 2*i
        A[it:it+2] = Ai
        i+=1
    # print(A)

    # compute svd and take smallest eigenvector
    U, D, VT = np.linalg.svd(A)
    # print(VT)
    H = VT[8]
    # reshape into 3*3 homography matrix
    H = np.reshape(H,(3,3))
    # print(H)

    # Denormalize H 
    H = np.matmul(np.matmul(np.linalg.pinv(T2),H),T1)
    # print(H)

    # we take the inverse homography matrix since we are doing reverse warping
    H = np.linalg.inv(H)

    newImg = imageWarp(np.array(image),np.array(newImg),H)
    newImg.show()
    newImg.save("topDownBasketballCourt.jpg")

if __name__ == "__main__":
    main()