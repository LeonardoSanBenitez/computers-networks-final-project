import RPi.GPIO as GPIO
import time
import numpy as np
from random import randrange
from random import choice
from picamera import PiCamera

class Sensor():
    pass

class Camera (Sensor):
    def __init__(self, imgWidht=800, imgHeight=800):
        self.imgWidht = imgWidht
        self.imgHeight = imgHeight
        self.camera = PiCamera()
        self.camera.resolution = (imgWidht, imgHeight)
        self.camera.framerate = 15
        self.camera.rotation = 90
        time.sleep(5)
        self.camera.start_preview()

    def captureFrame(self):
        print("begin readCamera...", end='')
        image = np.empty((self.imgHeight * self.imgWidht * 3,), dtype=np.uint8)
        self.camera.capture(image, 'bgr')
        image = image.reshape((self.imgHeight, self.imgWidht, 3))
        print("...Finishing readCamera")
        return image

    def __del__(self):
        self.camera.stop_preview()


class GY521 (Sensor):
    def __init__(self):
        pass
    def read(self, verbose=1):
        '''
        Brief: Communicate with MSP430 and get the INTEGRATED data
        Return: [(x,y), (dirX, dirY)]
        '''
        if verbose: print('begining readGY521...', end='')
        time.sleep(1)
        # TODO:
        if verbose: print("...Finishing readGY521")
        return [(randrange(10), randrange(10)), (randrange(-1, 2), randrange(-1, 2))]

class HCSR04 (Sensor):
    def __init__(self, gpioTrigger=6, gpioEcho=26):
        '''
        Careful: Echo pin needs 5V->3.3V conversion
        '''

        self.gpioTrigger = gpioTrigger
        self.gpioEcho = gpioEcho

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(gpioTrigger, GPIO.OUT)
        GPIO.setup(gpioEcho, GPIO.IN)


    def read(self, verbose=1):
        '''
        Return: distance in cm/s
        '''
        if verbose: print ('begining readHCSR...', end='')
        # set Trigger to HIGH
        GPIO.output(self.gpioTrigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpioTrigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.gpioEcho) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.gpioEcho) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        if verbose: print ('finished')
        return distance
