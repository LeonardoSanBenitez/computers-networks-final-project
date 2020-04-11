import concurrent.futures
from subprocess import Popen, PIPE
from random import randrange
from random import choice
from datetime import datetime
import os
import time
import cv2
import numpy as np
from picamera import PiCamera

from bme280 import Bme280
from adafruit_character_lcd import character_lcd
import board
import digitalio


class Flags:
    exportLog = True


def readGY521():
    # Communicate with MSP430 and get the INTEGRATED data
    # Return [(x,y), (dirX, dirY)]
    print("begin readGY521...")
    time.sleep(1)
    # TODO:
    print("...Finishing readGY521")
    return [(randrange(10), randrange(10)), (randrange(-1, 2), randrange(-1, 2))]

class Camera:
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
        print("begin readCamera...")
        image = np.empty((self.imgHeight * self.imgWidht * 3,), dtype=np.uint8)
        self.camera.capture(image, 'bgr')
        image = image.reshape((self.imgHeight, self.imgWidht, 3))
        print("...Finishing readCamera")
        return image

    def __del__(self):
        self.camera.stop_preview()


# TODO: This should be an specialization of RememberingPolicy class
class PolicyShape:
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

    def validate(self, image):
        self._processImg(image, thresh_value=110)

        # Take the biggest shape only
        shape, area = self._shapeBiggest()
        print('Found shape ', shape, 'of size ', area)
        if (shape != None):  # and area>areaThresh) #TODO: area threshold
            return True
        else:
            return False


class LCD():
    def __init__(self):
        # compatible with all versions of RPI as of Jan. 2019
        lcd_rs = digitalio.DigitalInOut(board.D16)
        lcd_en = digitalio.DigitalInOut(board.D12)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D23)
        lcd_d7 = digitalio.DigitalInOut(board.D18)

        self.lcd_columns = 16
        self.lcd_rows = 2
        lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                                               lcd_d6, lcd_d7, self.lcd_columns, self.lcd_rows)
        lcd.clear()
        time.sleep(2)
        print("LCD init OK\n")

    def update(self, message):
        lcd.clear()
        lcd.message = message


class Motor():
    def __init__(self):
        pass

    def move(self, speed):
        # Receve an speed, from -1 to 1
        pass

    def turn(self, angle):
        # Receive an angle to turn, from -180 to 180
        # angle=0 keep in the same direction
        pass


if __name__ == "__main__":
    explorationRange = 8
    flags = Flags()
    path_out = 'assets/'
    i=0

    lcd = LCD()
    motor = Motor()
    policy = PolicyShape()
    camera = Camera()
    executor = concurrent.futures.ThreadPoolExecutor()

    # Init BME
    bme280 = Bme280()
    (chip_id, chip_version) = bme280.readBME280ID()
    print("Sensor bme280 init OK")
    print("Chip ID     :" + str(chip_id))
    print("Version     :" + str(chip_version))

    while(1):
        future1 = executor.submit(readGY521)
        future2 = executor.submit(bme280.readBME280All)
        future3 = executor.submit(camera.captureFrame)

        while not (future1.done() & future2.done() & future3.done()):
            continue
        payload1 = future1.result()
        payload2 = future2.result()
        payload3 = future3.result()

        approved = policy.validate(payload3)
        if approved:
            # Found someting interesting
            mem = "memorable image"
            # Move randomly from -90 to -180 or 90 to 180
            motor.turn(randrange(90, 180)*choice([-1, 1]))
            motor.move(1)
        elif (payload1[0][0]**2 + payload1[0][1]**2) > explorationRange:
            # No object, but out of range
            mem = "nothing"
            # Move randomly from -135 to -180 or 135 to 180
            motor.turn(randrange(135, 180)*choice([-1, 1]))
            motor.move(1)
        else:
            # No object, still inside range
            mem = "nothing"

        # Local interface
        lcd_line_1 = "Memorable: " + str(future3.result())
        lcd_line_2 = "Temp.: " + str(future2.result()['temperature']) + " C"
        executor.submit(lcd.update, lcd_line_1 + '\n' + lcd_line_2)

        # TODO: send to server
        print(payload1[0], " = ", mem, ", with temperature ",
              payload2['temperature'], " C")
        print('-----------------')
        if flags.exportLog: 
            cv2.imwrite(path_out + 'img' + str(i) + '.jpg', payload3)
            print('saved ', i, 'image')
            i+=1
