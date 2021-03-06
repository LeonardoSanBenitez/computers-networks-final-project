import paho.mqtt.client as mqtt
import json
import base64

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("redesIFSC/benitez_nagel/device_0")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #payload = json.loads(msg.payload)
    #image_base64 = base64.decodebytes(payload['image'])
    #print('received', len(payload))
    print(msg.topic)#+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.username_pw_set('crojvinz', 'HKGvGSRSjC9B')
client.tls_set('comodorsacertificationauthority.crt')
client.tls_insecure_set(True)


client.connect("tailor.cloudmqtt.com", 20641, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

