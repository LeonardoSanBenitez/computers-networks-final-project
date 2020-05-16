import io
import numpy as np
import matplotlib.pyplot as plt
import requests
import cv2
import json


img = cv2.imread('../assets/last_image.jpg') # this is a numpy array
data = {'temperature': 666, 
        'haveImage': 1,
        'image': img.tolist()}
print(type(data))

headers = {'Content-Type': 'application/json'}
api_url = 'http://0.0.0.0:5000/receive/'

var_0 = requests.post(api_url, headers=headers, data=json.dumps(data))
