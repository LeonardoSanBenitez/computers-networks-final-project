from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import os

path_img = 'assets/'
path_log = 'assets/log.txt'

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
lcd_rs = digitalio.DigitalInOut(board.D16)
lcd_en = digitalio.DigitalInOut(board.D12)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, 
                                      lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.clear()
sleep(2)

print("LCD init OK\n")
while True:

    # Last image name
    list_of_videos = [path_img + i for i in os.listdir(path_img)] # List videos
    list_of_videos.sort(key=os.path.getctime) # Sort by creation time
    lcd_line_1 = list_of_videos[-1][len(path_img):len(path_img)+15] + '\n' # take the last, remove path, crop to 16
    
    # Last temperature from log
    f = open(path_log, "r")
    lcd_line_2 = f.readline()[:16]
    f.close()

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    #print("LCD update OK")
    sleep(2)