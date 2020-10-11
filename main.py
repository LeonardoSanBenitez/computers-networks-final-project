# Math and ML
import cv2
import numpy as np

# Utils 
import concurrent.futures
import json
from tempfile import TemporaryFile
import base64
import io

# AI modules
import perception
import reasoning
import interaction
import communication

FLAGS = {
    'exportLog': False,
    'alwaysMemorable': False,
    'sendMqtt': False,
    'sendHttp': False,
    'path_out': 'assets/',
    'verbose': 1
}

if __name__ == "__main__":
    bme280 = perception.Sensor_Bme280()
    motor = interaction.MotorUART()
    camera = perception.Camera(imgWidht=800, imgHeight=800)
    policy = reasoning.SelectionPolicyByObject(imgWidth=800, imgHeight=800)
    led = communication.LED()
    if FLAGS['sendMqtt']: mqtt = communication.MQTT(team='benitez_nagel', 
                              device='device_0', 
                              auth_user='crojvinz',
                              auth_pass='HKGvGSRSjC9B',
                              auth_cert='comodorsacertificationauthority.crt',
                              #auth_token='sQga6SL8ESsFvrbKbBkeLngDyflFHveXckV81w6vepYzE07FphKYvQrTUCnpYrd0',
                              broker_domain="tailor.cloudmqtt.com",#'mqtt.flespi.io',#"tailor.cloudmqtt.com",
                              broker_port=20641,#1883,#20641,
                              verbose=FLAGS['verbose'])
    if FLAGS['sendHttp']: http = HTTP(serverURL = 'http://192.168.0.51:5000/receive/')
    executor = concurrent.futures.ThreadPoolExecutor()
    if FLAGS['verbose']: print('Init done')
    
    i=0 #iteration count
    while(1):
        future_bme = executor.submit(bme280.readBME280All)
        future_camera = executor.submit(camera.captureFrame)
        concurrent.futures.wait([future_bme, future_camera], timeout=30)
        
        payload_bme = future_bme.result()
        payload_camera = future_camera.result()
        memorable_object = policy.validate(payload_camera)
        memorable = memorable_object or FLAGS['alwaysMemorable']
        if FLAGS['verbose'] and memorable: print('>>> Memorable obtect detected')
        if memorable:
            # TODO
            # policy.getDetections()
            # compare with image center: 
            #   error = (x_center - x_dog)
            #   control_sinal = error*C
            # variável de controle é o tempo (poderia ser a velocidade, mas eu resolvi simplificar)
            # send UART
            motor.send(motor.test_command(verbose=1))

        # Send to server
        data = {'temperature': payload_bme['temperature'],
                'pressure': payload_bme['pressure'],
                'humidity': payload_bme['humidity'],
                'haveImage': memorable}
        data = json.dumps(data)
        if FLAGS['verbose']: print('Sending... ' + data)
        if FLAGS['sendMqtt']: mqtt.send_json(data)

        file = TemporaryFile()
        np.save(file, payload_camera)
        file.seek(0)
        content = file.read()
        file.close()

        #data['image'] = str(base64.b64encode(content))
        #mqtt.send_image(base64.b64encode(content))
        #mqtt.send_image(bytearray(content))
         
        # Save in SD card
        if FLAGS['exportLog']: 
            cv2.imwrite(FLAGS['path_out'] + 'img' + str(i) + '.jpg', payload_camera)
            print('saved ', i, 'image')
            i+=1
        if FLAGS['verbose']: print('-----------------')
        led.toggle()
