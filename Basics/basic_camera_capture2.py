import time
import picamera
import numpy as np
import cv2

imgWidht = 320
imgHeight = 240



with picamera.PiCamera() as camera:
    camera.resolution = (imgWidht, imgHeight)
    camera.framerate = 24
    time.sleep(5)
    image = np.empty((imgHeight * imgWidht * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((imgHeight, imgWidht, 3))

    
    
cv2.imwrite('assets/TEST668.jpg', image)

