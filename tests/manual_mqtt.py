import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('emjyiozg', 'Dn0JR-tNjTg_')
client.tls_set('comodorsacertificationauthority.crt')
client.tls_insecure_set(True)
client.connect("soldier.cloudmqtt.com", 27040, 60)

i=0
while 1:
    client.publish('IFSC/redezinhas', payload='(%d) tá com cara de chuva, estou seguro'%i)
    i=i+1
    time.sleep(2)
