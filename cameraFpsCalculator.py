import cv2
import time
# Start default camera
def fpsVal():
    video = cv2.VideoCapture(0)
    num_frames = 120;

    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    for i in range(0, num_frames):
        ret, frame = video.read()
    end = time.time()

    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))
    return fps;

    # Release video
    video.release()

#print("after exeution")
val = fpsVal()
print(val)