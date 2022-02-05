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

def imageWarp(originalImg, newImg, H):
    original = np.array(originalImg)
    new = np.array(newImg)
    (row, col) = originalImg.size
    (w,h) = newImg.size
    for i in range(0,w):
        for j in range(0,h):
            coord = [i,j,1]
            # getting the warped coordinates
            res = np.matmul(H, coord)
            # print(res)
            # converting homogeneous coordinates back to regular inhomogeneous coords
            x = res[0]/res[2]
            y = res[1]/res[2]
            oxt = str(x).split('.')
            oyt = str(y).split('.')
            # print(x,y)
            if(len(oxt[1]) <= 1 or len(oyt[1]) <= 1):
                new[j][i] = original[int(x)][int(y)]
            else:
                pt_i = int(oyt[0])
                pt_j = int(oxt[0])
                a = float('0.'+oyt[1])
                b = float('0.'+oxt[1])
                if((pt_i+1) < row and (pt_j-1) >= 0):
                    red = (1-a)*(1-b)*original[pt_i][pt_j][0] + (a)*(1-b)*original[pt_i+1][pt_j][0] + (a)*(b)*original[pt_i+1][pt_j-1][0] + (1-a)*(b)*original[pt_i][pt_j-1][0]
                    green = (1-a)*(1-b)*original[pt_i][pt_j][1] + (a)*(1-b)*original[pt_i+1][pt_j][1] + (a)*(b)*original[pt_i+1][pt_j-1][1] + (1-a)*(b)*original[pt_i][pt_j-1][1]
                    blue = (1-a)*(1-b)*original[pt_i][pt_j][2] + (a)*(1-b)*original[pt_i+1][pt_j][2] + (a)*(b)*original[pt_i+1][pt_j-1][2] + (1-a)*(b)*original[pt_i][pt_j-1][2]
                    new[j][i] = [int(red), int(green), int(blue)]
    op_im = Image.fromarray(new)
    og_im = Image.fromarray(original)
    return op_im


def main():
    image = Image.open("basketball-court.ppm")
    # image.show()
    # print(image.size)
    newImg  = Image.new(mode = "RGB", size = (940, 500))
    # newImg.show()
    # [23,193] -> [0,0] 
    # [247,50] -> [940,0] 
    # [402,74] -> [940,500] 
    # [279,279] -> [0,500]
    arr1 = [[23,193,1],[247,50,1],[402,74,1],[279,279,1]]
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
    print(VT)
    H = VT[8]
    H = np.reshape(H,(3,3))
    # print(H)

    # Denormalize H 
    # H = np.matmul(np.linalg.inv(normalize(488,366)),np.matmul(H,normalize(940,500)))
    H = np.matmul(np.matmul(np.linalg.pinv(T2),H),T1)
    print(H)
    H = np.linalg.inv(H)

    result = imageWarp(image,newImg,H)
    result.show()

if __name__ == "__main__":
    main()