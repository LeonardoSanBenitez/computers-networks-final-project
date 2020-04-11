import concurrent.futures
from subprocess import Popen, PIPE
from time import sleep
from random import randrange
from random import choice
from datetime import datetime
import os

from bme280 import Bme280
from adafruit_character_lcd import character_lcd
import board
import digitalio

class Flags:
    exportLog = True
flags = Flags()




def readGY521():
    # Communicate with MSP430 and get the INTEGRATED data
    # Return [(x,y), (dirX, dirY)]
    print("begin readGY521...")
    sleep(1)
    #TODO: 
    print("...Finishing readGY521")
    return [(randrange(10), randrange(10)), (randrange(-1,2), randrange(-1,2))]


def readCamera():
    print("begin readCamera...")
    sleep(2)
    #TODO
    print("...Finishing readCamera")
    return randrange(2)

def readCamera():
    print("begin readCamera...")
    sleep(2)
    #TODO
    print("...Finishing readCamera")
    return randrange(2)

# TODO: This should be an specialization of RememberingPolicy class
class PolicyShape():
    _name = None
    def __init__(self, name='name'):
        self._name = name

    def validate(self, img):
        # do CV
        return True

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
    sleep(2)
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
  explorationRange=8
  executor = concurrent.futures.ThreadPoolExecutor()
  policy = PolicyShape()

  # Init BME
  bme280 = Bme280()
  (chip_id, chip_version) = bme280.readBME280ID()
  print("Sensor bme280 init OK")
  print("Chip ID     :" + str(chip_id))
  print("Version     :" + str(chip_version))

  lcd = LCD()
  motor = Motor()


  while(1):
      future1 = executor.submit(readGY521)
      future2 = executor.submit(bme280.readBME280All)
      future3 = executor.submit(readCamera)

      while not (future1.done() & future2.done() & future3.done()): continue
      payload1 = future1.result()
      payload2 = future2.result()
      payload3 = future3.result()
      if payload3: 
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

      #TODO: send to server
      print(payload1[0], " = ", mem, ", with temperature ",
            payload2['temperature'], " C")
      print('-----------------')
