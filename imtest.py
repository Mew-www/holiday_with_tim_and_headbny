from picamera.array import PiRGBArray
from picamera import PiCamera
import random
import time
import cv2
import numpy as np
import seaborn as sb

camera = PiCamera(resolution=(640,480), framerate=32)
rgb_array = PiRGBArray(camera)

# Let camera wake up a little
time.sleep(2)

def r_color(img, start_h, end_h, start_w, end_w):
    np.take(
        img[start_h:end_h, start_w:end_w, :],
        np.random.permutation(img[start_h:end_h, start_w:end_w, :].shape[2]),
        axis=2,
        out=img[start_h:end_h, start_w:end_w, :]
    )

def x_color(img, start_h, end_h, start_w, end_w, r, g, b):
    img[start_h:end_h, start_w:end_w, 0] = r*img[start_h:end_h, start_w:end_w, 0]
    img[start_h:end_h, start_w:end_w, 1] = b*img[start_h:end_h, start_w:end_w, 1]
    img[start_h:end_h, start_w:end_w, 2] = g*img[start_h:end_h, start_w:end_w, 2]

def flip(img, start_h, end_h, start_w, end_w):
    img[start_h:end_h, start_w:end_w, :] = np.rot90(
        img[start_h:end_h, start_w:end_w, :],
        random.randint(0,3),
        (0,1)
    )


palette = sb.color_palette("husl", 8)
for frame in camera.capture_continuous(rgb_array,
                                       format="bgr",
                                       use_video_port=True):
    img = frame.array.copy()
    #img = np.random.shuffle(img)
    for w in range(0, 640, 160):
        for h in range(0,480, 160):
            r, g, b = random.choice(palette)
            x_color(img, h, h+160, w, w+160, r, g, b)
            r_color(img, h, h+160, w, w+160)
            flip(img, h, h+160, w, w+160)
    cv2.imshow("RGB frame", img)
    key = cv2.waitKey(1) & 0xFF

    # Clear buffer
    rgb_array.truncate(0)

    if key == ord("q"):
        break
