from types import new_class
import numpy as np
import sys
import cv2
from PIL import Image

def rank_transform(image,win_size):
    trim = int((win_size-1)/2)
    w,h = image.shape
    rank = np.zeros((w,h))
    print(w,h)
    for i in range(0,w):
        for j in range(0,h):
            for x in range(i-trim,i+trim):
                for y in range(j-trim,j+trim):
                    if(0<=x<w and 0<=y<h):
                        if(image[x][y] < image[i][j]):
                            rank[i][j]+=1
    return rank



def main():
    image1 = Image.open("disp2.pgm")
    left = Image.open("teddyL.pgm")
    right = Image.open("teddyR.pgm")

    # image1.show()
    # left.show()
    # right.show()

    # apply rank transform to left and right images
    rank = rank_transform(np.array(left),5)
    print(rank)

if __name__ == "__main__":
    main()