'''
#%%
import ZedHandle
import cv2

camera = ZedHandle.ZedHandler()
camera.open()
camera.shoot()
camera.close()
cv2.imwrite('imgL.png', camera.imgL)
cv2.imwrite('imgR.png', camera.imgR)
# %%
print(camera.imgL)
'''
# %%
'''
from VisionHandle import VisionHandler, YoloDetector
import cv2
import os
detector = YoloDetector()
print(detector.cfg)
path = os.path.abspath(__file__)
path = os.path.dirname(path)
img_path = path + '/pics/good_data/01/left.png'
img = cv2.imread(img_path)
detector.detect(img)
'''
# %%
import cv2
import os
import time
from VisionHandle import VisionHandler
vision = VisionHandler(1, '123')
path = os.path.abspath(__file__)
path = os.path.dirname(path)
imgL_path = path + '/pics/good_data/01/left.png'
vision.imgL = cv2.imread(imgL_path)
imgR_path = path + '/pics/good_data/01/right.png'
vision.imgR = cv2.imread(imgR_path)
vision.camera.open()
vision.camera.close()
time0 = time.time()
vision.detectObject()
time1 = time.time()
print('detect time:',time1 - time0)
vision.getPos()
time2 = time.time()
print('getpos time:', time2 - time0)
print(vision.objPos)
#%%
import time
pipe_path = '/tmp/Vision.pipe'
try:
    os.mkfifo(pipe_path)
except OSError:
    print('[Info] VisionHandler: Pipe: ',pipe_path,' exists.')
pipe = os.open(pipe_path, os.O_CREAT | os.O_RDWR | os.O_NONBLOCK)
request = 'DetectObject;'
request += ' '*(200 - len(request))
os.write(pipe, request.encode('utf-8'))

# %%
