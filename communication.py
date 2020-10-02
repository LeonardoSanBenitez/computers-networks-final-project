import digitalio
from adafruit_character_lcd import character_lcd
import board
import time

class LCD():
    '''
    @Brief: local interface with LCD model xxx (TODO);
            Compatible with all versions of RPI as of Jan. 2019
    @Dependecy: adafruit_character_lcd
    @Code Example:
        lcd = LCD()
        lcd_line_1 = "Memorable: " + str(memorable)
        lcd_line_2 = "Temp.: " + str(future2.result()['temperature']) + " C"
        executor.submit(lcd.update, lcd_line_1 + '\n' + lcd_line_2)
    '''
    def __init__(self):
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


import paho.mqtt.client as mqtt
class MQTT():
    def _on_connect(self, userdata, flags, rc):
        '''
        The callback for when the client receives a CONNACK response from the server.
        '''
        if self._verbose: print("[MQTT] Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        #self._client.subscribe('redesIFSC/'+self._team+'/'+self._device)


    def _on_message(self, userdata, msg):
        '''
        @Brief: The callback for when a PUBLISH message is received from the server.
        '''
        if self._verbose: print("[MQTT] Command received: "+msg.topic+" "+str(msg.payload))
        
    def __init__(self, team, device, 
                 auth_user=None, auth_pass=None, auth_cert=None, 
                 broker_domain='broker.hivemq.com', broker_port=1883, 
                 verbose=0):
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        if auth_user and auth_pass:
            self._client.username_pw_set(auth_user, auth_pass)
        if auth_cert:
            self._client.tls_set(auth_cert)
            self._client.tls_insecure_set(True)
        self._team = team
        self._device = device
        self._verbose = verbose

        self._client.connect(broker_domain, broker_port, 60)

    def send(self, payload):
        self._client.publish('redesIFSC/'+self._team+'/'+self._device, payload=payload)

import requests
class HTTP():
    def __init__(self, serverURL, verbose=0):
        self._serverURL = serverURL
        self._verbose = verbose
        
    def send(self, payload):
        '''
        Expects a JSON formatted payload
        '''
        response = requests.post(self._serverURL,
                      headers={'Content-Type': 'application/json'},
                      data=payload)
        if self._verbose:
            print('[HTTP] Data sent, with response', response.status_code)
        return response.status_code


import RPi.GPIO as GPIO
class LED():
    def __init__(self, pin=16):
        self._pin = pin
        self._is_on = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUT, initial=GPIO.HIGH)
        
    def toggle(self):
        if self._is_on:
            GPIO.output(self._pin, GPIO.LOW)
            self._is_on = False
        else:
            GPIO.output(self._pin, GPIO.HIGH)
            self._is_on = True
