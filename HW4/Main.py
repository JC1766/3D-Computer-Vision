import numpy as np
from PIL import Image
import open3d as o3d


def main():
    d_dict = {}
    rgb_dict = {}
    for i in range(3):
        d_dict[i] = np.asarray(Image.open("problem1/depth" + str(i+1) + ".png"))
        rgb_dict[i] = (Image.open("problem1/rgb" + str(i+1) + ".png"))
        print(i)
    f = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    print(f)
    rgb_dict[2].show()
    # Compute the image derivates Ix and Iy
    # Then get Ix^2, Iy^2, and Ixy
    # Apply Gaussian smoothing to the derivatives using the 5x5 filter 
    # Compute the Harris operator response function for each pixel. 
    # Apply non-maximum suppression on the responses of the Harris operator in 3x3 windows.
    # Pick the 100 corners with the strongest response.



    
if __name__ == "__main__":
    main()