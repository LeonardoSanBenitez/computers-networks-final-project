from instance_segmentation import InstanceSegmentation
from flask import Flask, render_template, send_file, jsonify, request
import os
import sys
import json
import numpy as np
import cv2

app = Flask(__name__)
instance_segmentation = None
flags={'segment':False}

@app.route('/')
def home():
  #os.system('sshpass -p "123456" scp pi@raspberrypi.local:/home/pi/computers-networks-final-project/assets/last_image.jpg /home/benitez/Desktop/barn-dashboard/assets/')
  if flags['segment']: instance_segmentation.predict()
  print(f"Segmented model saved", file=sys.stdout)
  return render_template('home.html')

@app.route('/receive/', methods=['POST'])
def receive():
  print('request received')
  if not request.is_json:
    return 'The payload must be a JSON', 422
  content = request.get_json()
  temperature = content['temperature']
  print('Temperature is', temperature)
  if content['haveImage']==1:
    img = np.array(content['image'])
    print('read image with shape', img.shape)
    cv2.imwrite('assets/last_image.jpg', img)
  
  return 'thanks!', 200


@app.after_request
def set_response_headers(response):
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  return response

if __name__ == '__main__':
  if flags['segment']: 
    instance_segmentation = InstanceSegmentation(weight_path='predictive_models/mask_rcnn_coco.h5')
  print(f"RCNN model loaded", file=sys.stdout)
  app.run(debug=True, host='0.0.0.0')
