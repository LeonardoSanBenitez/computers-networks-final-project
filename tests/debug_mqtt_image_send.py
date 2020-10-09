#!/usr/bin/env python
# coding: utf-8

# In[65]:


import numpy as np
from tempfile import TemporaryFile
import base64
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
                 auth_user=None, auth_pass=None, auth_cert=None, auth_token=None,
                 broker_domain='broker.hivemq.com', broker_port=1883, 
                 verbose=0):
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        if auth_user and auth_pass:
            self._client.username_pw_set(auth_user, auth_pass)
        if auth_token:
            self._client.username_pw_set(auth_token)
        if auth_cert:
            self._client.tls_set(auth_cert)
            self._client.tls_insecure_set(True)
        self._team = team
        self._device = device
        self._verbose = verbose

        self._client.connect(broker_domain, broker_port, 60)

    def send_json(self, payload):
        self._client.publish('redesIFSC/'+self._team+'/'+self._device+'/json', payload=payload)
    def send_image(self, payload):
        self._client.publish('redesIFSC/'+self._team+'/'+self._device+'/image', payload=payload)

my_mqtt = MQTT(team='benitez_nagel', 
              device='device_0', 
              #auth_user='crojvinz',
              #auth_pass='HKGvGSRSjC9B',
              #auth_cert='comodorsacertificationauthority.crt',
              auth_token='sQga6SL8ESsFvrbKbBkeLngDyflFHveXckV81w6vepYzE07FphKYvQrTUCnpYrd0',
              broker_domain="mqtt.flespi.io",#'mqtt.flespi.io',#"tailor.cloudmqtt.com",
              broker_port=1883,#1883,#20641,
              verbose=0)

payload_camera = np.ones([10, 10])
file = TemporaryFile()
np.save(file, payload_camera)
file.seek(0)
content = file.read()
file.close()

my_mqtt.send_image(base64.b64encode(content))

