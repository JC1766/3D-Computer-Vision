import numpy as np
import open3d as o3d
import cv2
import math


def gaussian(im, size):
    sigma = (size - 1) / 6
    # center = sigma*3 + 1
    g = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            g[i, j] = math.exp(-((i) ** 2 + (j) ** 2) / (2 * sigma ** 2)) / (2 * math.pi * sigma ** 2)
    return cv2.filter2D(im, -1, g)

def calc_moment_matrix(im):
    im_ar = np.asarray(im)
    r, c = im_ar.shape
    im_xx_ar = np.zeros((r, c))
    im_yy_ar = np.zeros((r, c))
    im_xy_ar = np.zeros((r, c))
    im_xxg_ar = gaussian(im_xx_ar, 5)
    im_yyg_ar = gaussian(im_yy_ar, 5)
    im_xyg_ar = gaussian(im_xy_ar, 5)
    mat = [[[] for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):
            mat[i][j] = [im_xxg_ar[i][j], im_xyg_ar[i][j], im_yyg_ar[i][j]]
    return mat



def main():
    d_dict = {}
    rgb_dict = {}
    for i in range(3):
        d_dict[i] = cv2.imread("problem1/depth" + str(i + 1) + ".png")
        rgb_dict[i] = cv2.imread("problem1/rgb" + str(i + 1) + ".png")
    xkernel = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    ykernel = np.transpose(xkernel)
    print(ykernel)
    # Compute the image derivates Ix and Iy
    # Then get Ix^2, Iy^2, and Ixy
    x1 = cv2.filter2D(rgb_dict[0], -1, xkernel)
    x2 = cv2.filter2D(rgb_dict[1], -1, xkernel)
    x3 = cv2.filter2D(rgb_dict[2], -1, xkernel)

    y1 = cv2.filter2D(rgb_dict[0], -1, ykernel)
    y2 = cv2.filter2D(rgb_dict[1], -1, ykernel)
    y3 = cv2.filter2D(rgb_dict[2], -1, ykernel)

    xx1 = cv2.filter2D(x1, -1, xkernel)
    xx2 = cv2.filter2D(x2, -1, xkernel)
    xx3 = cv2.filter2D(x3, -1, xkernel)

    xy1 = cv2.filter2D(y1, -1, xkernel)
    xy2 = cv2.filter2D(y2, -1, xkernel)
    xy3 = cv2.filter2D(y3, -1, xkernel)

    yy1 = cv2.filter2D(y1, -1, ykernel)
    yy2 = cv2.filter2D(y2, -1, ykernel)
    yy3 = cv2.filter2D(y3, -1, ykernel)
    cv2.imshow("x1", x1)
    cv2.waitKey(0)
    cv2.imshow("y1", y1)
    cv2.waitKey(0)
    cv2.imshow("xx1", xx1)
    cv2.waitKey(0)
    cv2.imshow("xy1", xy1)
    cv2.waitKey(0)
    cv2.imshow("yy1", yy1)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Apply Gaussian smoothing to the derivatives using the 5x5 filter

    # Compute the Harris operator response function for each pixel.
    # Apply non-maximum suppression on the responses of the Harris operator in 3x3 windows.
    # Pick the 100 corners with the strongest response.
    #print(x1)

if __name__ == "__main__":
    main()