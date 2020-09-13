# Math and ML
import cv2
import numpy as np

# Utils 
import concurrent.futures
from subprocess import Popen, PIPE
from random import randrange
from random import choice
import json

# AI modules
import perception
import reasoning
import interaction
import communication

FLAGS = {
    'exportLog': False,
    'alwaysMemorable': True,
    'sendMqtt': True,
    'sendHttp': False,
    'verbose': 1
}

if __name__ == "__main__":
    explorationRange = 8
    path_out = 'assets/' 
    
    #hcsr04 = perception.Sensor_HCSR04()
    #gy521 = perception.Sensor_GY521()
    bme280 = perception.Sensor_Bme280()
    motor = interaction.MotorUART()
    camera = perception.Camera()
    policy1 = reasoning.SelectionPolicyByShape()
    policy2 = reasoning.SelectionPolicyByDistance(threshold=10)
    led = communication.LED()
    mqtt = communication.MQTT(team='benitez_nagel', device='device_0', verbose=FLAGS['verbose'])
    #http = HTTP(serverURL = 'http://192.168.0.51:5000/receive/')
    executor = concurrent.futures.ThreadPoolExecutor()
    if FLAGS['verbose']: print('Init done')
    
    i=0 #iteration count
    while(1):
        #TODO: give more descriptive names
        future2 = executor.submit(bme280.readBME280All)
        future3 = executor.submit(camera.captureFrame)
        concurrent.futures.wait([future2, future3], timeout=5)
        
        payload2 = future2.result()
        payload3 = future3.result()

        good_frame = policy1.validate(payload3)
        #too_close = policy2.validate(payload4)
        memorable = False#good_frame or too_close or FLAGS['alwaysMemorable']
        if memorable:
            # Found someting interesting
            # Move randomly from -90 to -180 or 90 to 180
            motor.turn(randrange(90, 180)*choice([-1, 1]))
            motor.move(1)
        #elif (payload1[0][0]**2 + payload1[0][1]**2) > explorationRange:
        #    # No object, but out of range
        #    # Move randomly from -135 to -180 or 135 to 180
        #    motor.turn(randrange(135, 180)*choice([-1, 1]))
        #    motor.move(1)
        else:
            # No object, still inside range
            pass

        # Send to server
        #data = {#'position': payload1[0],
        #        #'direction': payload1[1],
        #        'temperature': payload2['temperature'],
        #        'haveImage': memorable}
        data = {'temp': payload2['temperature']}
        if memorable:
            data['image'] = payload3.tolist()
        data = json.dumps(data)

        if FLAGS['verbose']: print('Sending... '+data)
        mqtt.send(data)
        #http.send(data)

        # Save in SD card
        if FLAGS['exportLog']: 
            cv2.imwrite(path_out + 'img' + str(i) + '.jpg', payload3)
            print('saved ', i, 'image')
            i+=1
        print('-----------------')
        led.toggle()
