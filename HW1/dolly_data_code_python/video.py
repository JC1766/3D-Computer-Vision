import cv2
import os

def main():
    image_folder = './'
    video_name = 'video.wmv'

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 15, (width,height))

    for i in range(0,75):
        video.write(cv2.imread(os.path.join(image_folder, "SampleOutput"+str(i)+".jpg")))
    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    main()