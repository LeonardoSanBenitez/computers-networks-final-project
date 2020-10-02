# Math and ML
import cv2
import numpy as np

# Utils 
import concurrent.futures
import json
from tempfile import TemporaryFile
import base64

# AI modules
import perception
import reasoning
import interaction
import communication

FLAGS = {
    'exportLog': True,
    'alwaysMemorable': True,
    'sendMqtt': True,
    'sendHttp': False,
    'path_out': 'assets/',
    'verbose': 1
}

if __name__ == "__main__":
    bme280 = perception.Sensor_Bme280()
    motor = interaction.MotorUART()
    camera = perception.Camera()
    policy = reasoning.SelectionPolicyByShape()
    led = communication.LED()
    
    mqtt = communication.MQTT(team='benitez_nagel', 
                              device='device_0', 
                              #auth_user='crojvinz',
                              #auth_pass='HKGvGSRSjC9B',
                              #auth_cert='comodorsacertificationauthority.crt',
                              auth_token='sQga6SL8ESsFvrbKbBkeLngDyflFHveXckV81w6vepYzE07FphKYvQrTUCnpYrd0',
                              broker_domain='mqtt.flespi.io',#"tailor.cloudmqtt.com",
                              broker_port=1883,#20641,
                              verbose=FLAGS['verbose'])
    #http = HTTP(serverURL = 'http://192.168.0.51:5000/receive/')
    executor = concurrent.futures.ThreadPoolExecutor()
    if FLAGS['verbose']: print('Init done')
    
    i=0 #iteration count
    while(1):
        future_bme = executor.submit(bme280.readBME280All)
        future_camera = executor.submit(camera.captureFrame)
        concurrent.futures.wait([future_bme, future_camera], timeout=5)
        
        payload_bme = future_bme.result()
        payload_camera = future_camera.result()

        memorable_object = policy.validate(payload_camera)
        memorable = memorable_object or FLAGS['alwaysMemorable']
        if memorable:
            #TODO
            # policy.getDetections()
            # compare with image center
            # propotional control
            # send UART
            pass

        # Send to server
        data = {'temperature': payload_bme['temperature'],
                'pressure': payload_bme['pressure'],
                'humidity': payload_bme['humidity'],
                'haveImage': memorable}
        if FLAGS['verbose']: print('Sending... ' + json.dumps(data))#print without image, otherwise...
        


        if memorable:
        #    data['image'] = payload_camera.tolist()
            with TemporaryFile() as f:
                np.save(f, payload_camera)
                s = base64.b64encode(f)
                data['image'] = s
        data = json.dumps(data)

        mqtt.send(data)
        #http.send(data)

        # Save in SD card
        if FLAGS['exportLog']: 
            cv2.imwrite(FLAGS['path_out'] + 'img' + str(i) + '.jpg', payload_camera)
            print('saved ', i, 'image')
            i+=1
        if FLAGS['verbose']: print('-----------------')
        led.toggle()
