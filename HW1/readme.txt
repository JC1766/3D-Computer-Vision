CS532 Homework 1
Part 1: Apply Normalized DLT algorithm for homography estimation and use binlinear interpolation for rendering output image.

To start off, we first choose four points on the original baskeball court image to select only the playing court itself, which we know is a rectangle shape.
# [23,193] -> [0,0] 
# [247,51] -> [939,0] 
# [402,74] -> [939,499] 
# [279,279] -> [0,499]
We want to map the court to a 940*500 canvas to portray a topdown view of the basketball court, and to do that we use the DLT algorithm to obtain the homography matrix which we then inversed as we will be using reverse warping. For each pixel in the new canvas, the corresponding pixel location is obtained using the homography matrix and if the location is between pixels, we use bilinear interpolation to sample the color of each surrounding pixel. The resulting image will give us a topdown view of the basketball court area that we selected from the original image.


Part 2: Design a sequence of projection matrices corresponding to each frame of a "dolly zoom" capture sequence and effect.

The Dolly Zoom effect is obtained by adjusting the zoom angle of the camera in the opposite direction while moving the camera position forward or backwards. Our starting point, or origin in the image is around 4 meters from the foreground object, which displays it in a 250*400 box. To display the foreground object in a 400*640 box instead, we have to move the camera position forward by 1.44 meters obtained from the ratio 8/5 * the length of projection 9 meters. As for the zoom adjustment in each step to maintain the size of the foreground object while moving forward or backwards, we have to change the values of rx and ry in the internal calibration matrix K using the formula y = f*Y/Z where Y, Z are the initial values of [rx or ry] and [distance] respectively and y, f are the current values. The starting position of the image is now 1.44m away from the origin, so for the first video we zoom in while moving backwards from the object to return to the origin, with each step being 0.0192m obtained from 1.44 distance / 75 frames. The second video simply performs the zoom in the other direction.
