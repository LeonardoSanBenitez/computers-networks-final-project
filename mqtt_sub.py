import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("redesIFSC/benitez_nagel/device_0/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    # print(f"received in topic: {msg.topic}")
    print(f"{msg.topic}: {msg.payload}")

    subtopic = msg.topic.split('/')[-1]

    # telemetry data
    if subtopic == 'json':
        with open("./web_server/data/telemetry.json", "w") as file:
            telemetry = json.loads(str(msg.payload, 'utf-8'))
            if 'haveImage' in telemetry:
                del telemetry['haveImage'] 

            file.write(json.dumps(telemetry))
    

    # image data
    elif subtopic == 'image':
        print("")
    
    else:
        print("Invalid topic")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set('comodorsacertificationauthority.crt')
client.username_pw_set('crojvinz', 'HKGvGSRSjC9B')

client.connect("tailor.cloudmqtt.com", 20641, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

