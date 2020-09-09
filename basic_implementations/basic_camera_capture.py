import time
from picamera import PiCamera

camera = PiCamera()

camera.start_preview()
time.sleep(5)
camera.capture('assets/TEST2.jpg')
camera.stop_preview()

f = open("assets/log.txt", "a")
f.write("img saved\n")
f.close()
