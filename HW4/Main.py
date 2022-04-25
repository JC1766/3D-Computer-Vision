import numpy as np
from PIL import Image
import open3d as o3d


def main():
    print("hi")

    # Compute the image derivates Ix and Iy
    # Then get Ix^2, Iy^2, and Ixy
    # Apply Gaussian smoothing to the derivatives using the 5x5 filter 
    # Compute the Harris operator response function for each pixel. 
    # Apply non-maximum suppression on the responses of the Harris operator in 3x3 windows.
    # Pick the 100 corners with the strongest response.

    
if __name__ == "__main__":
    main()