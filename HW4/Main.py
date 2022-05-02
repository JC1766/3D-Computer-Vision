import numpy as np
import open3d as o3d
import cv2
import math

def gaussian(im,size):
    sigma = (size-1)/6
    # center = sigma*3 + 1
    g = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            g[i,j] = math.exp(-((i)**2+(j)**2)/(2*sigma**2))/(2*math.pi*sigma**2)
    return cv2.filter2D(im,-1,g)
def suppression(im):
    ht,wd = im.shape
    result = np.zeros((ht,wd))
    for i in range(2,(ht - 1)):
        for j in range(2,(wd - 1)):
            nb = im[i-1:i+1, j-1:j+1]
            if(im[i,j] == nb.max()):
                result[i,j] = im[i,j]
    return result
def main():
    d_dict = {}
    rgb_dict = {}
    g_dict = {}
    for i in range(3):
        d_dict[i] = cv2.imread("problem1/depth" + str(i+1) + ".png")
        rgb_dict[i] = cv2.imread("problem1/rgb" + str(i+1) + ".png")
        g_dict[i] = cv2.cvtColor(rgb_dict[i], cv2.COLOR_BGR2GRAY)
    xkernel = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    ykernel = np.transpose(xkernel)
    print(ykernel)
    # Compute the image derivates Ix and Iy
    # Then get Ix^2, Iy^2, and Ixy
    x1 = cv2.filter2D(g_dict[0],-1,xkernel)
    x2 = cv2.filter2D(g_dict[1],-1,xkernel)
    x3 = cv2.filter2D(g_dict[2],-1,xkernel)

    y1 = cv2.filter2D(g_dict[0],-1,ykernel)
    y2 = cv2.filter2D(g_dict[1],-1,ykernel)
    y3 = cv2.filter2D(g_dict[2],-1,ykernel)

    xx1 = cv2.filter2D(x1,-1,xkernel)
    xx2 = cv2.filter2D(x2,-1,xkernel)
    xx3 = cv2.filter2D(x3,-1,xkernel)

    xy1 = cv2.filter2D(y1,-1,xkernel)
    xy2 = cv2.filter2D(y2,-1,xkernel)
    xy3 = cv2.filter2D(y3,-1,xkernel)

    yy1 = cv2.filter2D(y1,-1,ykernel)
    yy2 = cv2.filter2D(y2,-1,ykernel)
    yy3 = cv2.filter2D(y3,-1,ykernel)
    # cv2.imshow("x1", x1)
    # cv2.imshow("y1", y1)
    # cv2.imshow("xx1", xx1)
    # cv2.imshow("xy1", xy1)
    # cv2.imshow("yy1", yy1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    

    # Apply Gaussian smoothing to the derivatives using the 5x5 filter 
    gxx1 = gaussian(xx1,5)
    gxx2 = gaussian(xx2,5)
    gxx3 = gaussian(xx3,5)

    gxy1 = gaussian(xy1,5)
    gxy2 = gaussian(xy2,5)
    gxy3 = gaussian(xy3,5)

    gyy1 = gaussian(yy1,5)
    gyy2 = gaussian(yy2,5)
    gyy3 = gaussian(yy3,5)
    cv2.imshow("xx1", xx1)
    cv2.imshow("xy1", xy1)
    cv2.imshow("yy1", yy1)
    cv2.imshow("gxx1", gxx1)
    cv2.imshow("gxy1", gxy1)
    cv2.imshow("gyy1", gyy1)
    cv2.waitKey(0)
    # Compute the Harris operator response function for each pixel. 
    # R = det(M) - alpha*trace(M)^2
    a = 0.05
    # print(gxx1.shape, gyy1.shape)
    r1 = np.multiply(gxx1,gyy1)
    r1 = (np.multiply(gxx1,gyy1) - np.square(gxy1,gxy1)) - a*np.square(gxx1+gyy1)
    cv2.imshow("r1", r1)
    cv2.waitKey(0)
    s1 = suppression(r1)
    cv2.imshow("s1", s1)
    cv2.waitKey(0)

    # Apply non-maximum suppression on the responses of the Harris operator in 3x3 windows.
    # Pick the 100 corners with the strongest response.



    
if __name__ == "__main__":
    main()