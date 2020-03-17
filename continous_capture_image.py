#!/usr/bin/env python
# coding: utf-8

# Based on https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/

# In[1]:


# Global variables
path_out = 'assets/'
path_in = 'assets/image2.jpg' # in case we are reading from disk, not from camera

imgWidht = 320
imgHeight = 240

class Flags:
    export = True
    onRaspberry = False
flags=Flags()   


# In[2]:


import cv2
import numpy as np

if flags.onRaspberry:
    import time
    from picamera import PiCamera
else:
    import matplotlib.pyplot as plt


# In[22]:


class ShapeDetector:
    contours = None
    image = None

    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # return the name of the shape
        return shape

    def processImg(self, image, thresh_value=60):
        # convert the resized image to grayscale, blur it slightly, and threshold it
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, thresh_value, 255, cv2.THRESH_BINARY)[1]
        _, self.contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.image = image.copy()
        return thresh
    
    def shapeBiggest (self):
        assert self.contours!=None, ('processed image first')
        if len(self.contours) != 0:
            c = max(self.contours, key = cv2.contourArea) #find the biggest area
            area = cv2.contourArea(c)
            shape = self.detect(c)
        else:
            shape='none'
            area=0
        return shape, area
    def shapeAll (self, verbose=1):
        assert type(self.image)!=type(None), ('processed image first')
        img_labels = self.image.copy()
        n=0
        for c in self.contours:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            cX = int((M["m10"] / (M["m00"]+1)))
            cY = int((M["m01"] / (M["m00"]+1)))
            shape = self.detect(c)

            cv2.drawContours(img_labels, [c], -1, (0, 255, 0), 2)
            cv2.putText(img_labels, shape, (cX, cY), 
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            # show the output img_labels
            if verbose>0: print('Shape ' + str(n) + '=' + shape + "\t\t Area=" + str(cv2.contourArea(c)))
            n+=1
        return img_labels
sd = ShapeDetector()


# In[41]:


i=0
while (1):
    # Read Image
    if flags.onRaspberry:
        with PiCamera() as camera:
            camera.resolution = (imgWidht, imgHeight)
            camera.framerate = 25
            camera.start_preview()
            time.sleep(2) # warm up time
            image = np.empty((imgWidht, imgHeight, 3), dtype=np.uint8)
            camera.capture(image, 'rgb')
            camera.stop_preview()
            print("Image captured, shape " + str(image.shape))
    else:
        image = cv2.imread(path_in)
        image = cv2.resize(image, (imgWidht, imgHeight), interpolation = cv2.INTER_LINEAR)
        plt.imshow(image)

    # Process image
    thresh = sd.processImg(image, thresh_value=110)#np.zeros((imgWidht, imgHeight, 3), dtype=np.uint8))#test 
    print ('Image thresholded, pixel\'s mean: ' + str(thresh.mean()))
    if not flags.onRaspberry: plt.imshow(thresh)
    
    # Take the biggest shape only
    shape, area = sd.shapeBiggest()
    print("Biggest shape=" + shape + "\nArea=" + str(area))
    if flags.export: cv2.imwrite(path_out + 'img' + str(i) + '_' + shape + '.jpg', image)
        
    # Take all the shapes
    #img_labels = sd.shapeAll()
    #if not flags.onRaspberry: plt.imshow(cv2.cvtColor(img_labels, cv2. COLOR_BGR2RGB))
    #if flags.export: cv2.imwrite(path_out + 'img' + str(i) + '_labels.jpg', img_labels)
        
    if flags.onRaspberry:
        i+=1
        print('------------------------------------')
    else:
        break


# In[4]:


if not flags.onRaspberry:
    get_ipython().system("jupyter nbconvert --output 'continous_capture_image' --to script 01\\ -\\ Embedded\\ shape\\ detector.ipynb")

