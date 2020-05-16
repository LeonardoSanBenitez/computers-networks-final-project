# Math and ML
import cv2
import numpy as np

# Utils 
import concurrent.futures
from subprocess import Popen, PIPE
from random import randrange
from random import choice
from datetime import datetime
import os
import time

# hardware, sensors and actuators
import board
import digitalio
from picamera import PiCamera
from adafruit_character_lcd import character_lcd
import SelectionPolicy
import Sensor

# Web
import requests
import json


class Flags:
    exportLog = False
    alwaysMemorable = True

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
            pass# PWM1_DIR = foward
            # PWM1=speed

            # PWM2_DIR = foward
            # PWM2=speed
        elif speed<0:
            pass# PWM1_DIR = backward
            # PWM1=speed

            # PWM2_DIR = backward
            # PWM2=speed
        else:
            pass# PWM1=0
            # PWM2=0

    def turn(self, angle):
        # Receive an angle to turn, from -180 to 180
        # angle=0 keep in the same direction
        if angle>0:
            pass# PWM1_DIR = foward
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
    serverURL = 'http://192.168.0.51:5000/receive/'
    i=0

    hcsr04 = Sensor.HCSR04()
    gy521 = Sensor.GY521()
    bme280 = Sensor.Bme280()
    lcd = LCD()
    motor = Motor()
    camera = Sensor.Camera()
    policy1 = SelectionPolicy.Shape()
    policy2 = SelectionPolicy.Distance(threshold=10)
    
    executor = concurrent.futures.ThreadPoolExecutor()

    while(1):
        future1 = executor.submit(gy521.read)
        future2 = executor.submit(bme280.readBME280All)
        future3 = executor.submit(camera.captureFrame)
        future4 = executor.submit(hcsr04.read)

        #while not (future1.done() & future2.done() & future3.done() & future4.done()):
        #    continue
        concurrent.futures.wait([future1, future2, future3, future4], timeout=5)
        payload1 = future1.result()
        payload2 = future2.result()
        payload3 = future3.result()
        payload4 = future4.result()

        good_frame = policy1.validate(payload3)
        too_close = policy2.validate(payload4)
        memorable = good_frame or too_close or flags.alwaysMemorable
        if memorable:
            # Found someting interesting
            # Move randomly from -90 to -180 or 90 to 180
            motor.turn(randrange(90, 180)*choice([-1, 1]))
            motor.move(1)
        elif (payload1[0][0]**2 + payload1[0][1]**2) > explorationRange:
            # No object, but out of range
            # Move randomly from -135 to -180 or 135 to 180
            motor.turn(randrange(135, 180)*choice([-1, 1]))
            motor.move(1)
        else:
            # No object, still inside range
            pass

        # Local interface
        lcd_line_1 = "Memorable: " + str(memorable)
        lcd_line_2 = "Temp.: " + str(future2.result()['temperature']) + " C"
        executor.submit(lcd.update, lcd_line_1 + '\n' + lcd_line_2)

        # Print in terminal
        print('Position:', payload1[0])
        print('Direction:', payload1[1])
        print('Temperature:', payload2['temperature'], 'C')
        print('Memorable:', memorable)
        print("Distance:", payload4)
        

        # Send to server
        data = {'position': payload1[0],
                'direction': payload1[1],
                'temperature': payload2['temperature'],
                'haveImage': memorable}
        if memorable:
            data['image'] = impayload3g.tolist()

        respose = requests.post(serverURL, 
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(data))
        print('Data sent, with response', response.status_code)
        # TODO Send takes to much, I think I should put it as a thread

        # Save in SD card
        if flags.exportLog: 
            cv2.imwrite(path_out + 'img' + str(i) + '.jpg', payload3)
            print('saved ', i, 'image')
            i+=1
        print('-----------------')
