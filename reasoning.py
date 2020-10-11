import cv2
import numpy as np


class SelectionPolicy():
    def __init__(self):
        pass

    def validate(self):
        return True


class SelectionPolicyByShape (SelectionPolicy):
    contours = None
    image = None

    def __init__(self):
        pass

    def _detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or a rectangle
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
        elif len(approx) == 6:
            shape = "hexagon"
        else:
            shape = None
        # return the name of the shape
        return shape

    def _processImg(self, image, thresh_value=60):
        # convert the resized image to grayscale, blur it slightly, and threshold it
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, thresh_value,
                               255, cv2.THRESH_BINARY)[1]
        _, self.contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.image = image.copy()
        return thresh

    def _shapeBiggest(self):
        assert self.contours != None, ('processed image first')
        if len(self.contours) != 0:
            # find the biggest area
            c = max(self.contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            shape = self._detect(c)
        else:
            shape = None
            area = 0
        return shape, area

    def _shapeAll(self, verbose=1):
        assert type(self.image) != type(None), ('processed image first')
        img_labels = self.image.copy()
        n = 0
        for c in self.contours:
            # compute the center of the contour, then _detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            cX = int((M["m10"] / (M["m00"]+1)))
            cY = int((M["m01"] / (M["m00"]+1)))
            shape = self._detect(c)

            cv2.drawContours(img_labels, [c], -1, (0, 255, 0), 2)
            cv2.putText(img_labels, shape, (cX, cY),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
            # show the output img_labels
            if verbose > 0:
                print('Shape ' + str(n) + '=' + shape +
                      "\t\t Area=" + str(cv2.contourArea(c)))
            n += 1
        return img_labels

    def validate(self, image, verbose=0):
        self._processImg(image, thresh_value=110)

        # Take the biggest shape only
        shape, area = self._shapeBiggest()
        if verbose: print('Found shape ', shape, 'of size ', area)
        if (shape != None):  # and area>areaThresh) #TODO: area threshold
            return True
        else:
            return False


class SelectionPolicyByDistance(SelectionPolicy):
    '''
    Brief: Receive distance in cm/s
    '''

    threshold = None

    def __init__(self, threshold):
        self.threshold = threshold

    def validate(self, distance):
        '''
        Brief: momento is memorable if distance<thresh (object is too close)
        Return: boolean
        '''
        if distance < self.threshold:
            return True
        else:
            return False


class SelectionPolicyByObject (SelectionPolicy):
    '''
    Based on: https://towardsdatascience.com/face-detection-in-2-minutes-using-opencv-python-90f89d7c0f81
    Return: bool
    '''
    imgWidth = None
    imgHeight = None

    def __init__(self, imgWidth=320, imgHeight=240, path_model='assets/models/haarcascade_frontalface_default.xml'):
        '''
        @Brief: the object to be detected is defined by the cascade model passed
        '''
        self.imgHeight = imgHeight
        self.imgWidth = imgWidth
        self.cascade_model = cv2.CascadeClassifier(path_model)

    def validate(self, img, verbose=0):
        assert type(img) != type(None), ('invalid image')

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        self._detections = self.cascade_model.detectMultiScale(gray, 1.3, 5)
        if verbose: print(self._detections)
        if len(self._detections) > 0:
            return True
        else:
            return False
        
    def getDetections(self):
        return self._detections



class SelectionPolicyByMovement(SelectionPolicy):
    def __init__(self):
        raise Exception('not implemented')

    def validate(self, img):
        #if |last_img - img| > threshold then policy = true
        #self.last_img=img
        pass
