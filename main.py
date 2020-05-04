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

import SelectionPolicy
import Sensor


class Flags:
    exportLog = True

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
    # We'll need to use an Dual 1-of-4 Demultiplexer, because Raspbery only have 2 PWMs
    # Tutorial: https://circuitdigest.com/microcontroller-projects/raspberry-pi-pwm-tutorial
    def __init__(self):
        pass

    def move(self, speed):
        # Brief: Receve an speed, from -1 to 1
        # Return: nothing

        if speed>0:
            # PWM1_DIR = foward
            # PWM1=speed

            # PWM2_DIR = foward
            # PWM2=speed
        elif speed<0:
            # PWM1_DIR = backward
            # PWM1=speed

            # PWM2_DIR = backward
            # PWM2=speed
        else:
            # PWM1=0
            # PWM2=0

    def turn(self, angle):
        # Receive an angle to turn, from -180 to 180
        # angle=0 keep in the same direction
        if angle>0:
            # PWM1_DIR = foward
            # PWM1=255
            # PWM2_DIR = backward
            # PWM2=255
            # wait xxx time (heuristic)
            # PWM1=0
            # PWM2=0
        elif angle<0:
        pass


if __name__ == "__main__":
    explorationRange = 8
    flags = Flags()
    path_out = 'assets/'
    i=0

    gy521 = GY521()
    lcd = LCD()
    motor = Motor()
    policy1 = SelectionPolicy.Shape()
    policy2 = SelectionPolicy.Distance(threshold=10)
    camera = Camera()
    executor = concurrent.futures.ThreadPoolExecutor()

    # Init BME
    bme280 = Bme280()
    (chip_id, chip_version) = bme280.readBME280ID()
    print("Sensor bme280 init OK")
    print("Chip ID     :" + str(chip_id))
    print("Version     :" + str(chip_version))

    while(1):
        future1 = executor.submit(gy521.read)
        future2 = executor.submit(bme280.readBME280All)
        future3 = executor.submit(camera.captureFrame)
        future4 = executor.submit(hcsr04.read)

        while not (future1.done() & future2.done() & future3.done() & future4.done()):
            continue
        payload1 = future1.result()
        payload2 = future2.result()
        payload3 = future3.result()
        payload4 = future3.result()

        good_frame = policy1.validate(payload3)
        too_close = policy2.validate(payload4)
        if good_frame or too_close:
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
