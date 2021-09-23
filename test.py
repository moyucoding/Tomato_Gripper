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
import numpy as np
camX = 15
camY = 0
camZ = 0
camPos = np.array([camX,camY,camZ,1])
camPos.reshape((1,4))
print(camPos)
'''
r1 = np.array([ [ 0, 0, 1,  0],
                [-1, 0, 0,  0],
                [ 0,-1, 0, 10],
                [ 0, 0, 0,  1]])
'''
r1 = np.array([ [ 1, 0, 0,  0],
                [ 0, 1, 0,-10],
                [ 0, 0, 1,  0],
                [ 0, 0, 0,  1]])
print(r1.dot(camPos))

#Rotation 2: TCP to Base
tcp = (0,0,0,0,1.57,0)
x ,y ,z ,rx ,ry ,rz = tcp
r2 = np.zeros((4,4))
cosx = np.cos(rx)
sinx = np.sin(rx)
cosy = np.cos(ry)
siny = np.sin(ry)
cosz = np.cos(rz)
sinz = np.sin(rz)

r2 = np.array( [[cosy*cosz, sinx*siny*cosz - cosx*sinz, cosx*siny*cosz + sinx*sinz, x],
                [cosy*sinz, sinx*siny*sinz + cosx*cosz, cosx*siny*sinz - sinx*cosz, y],
                [    -siny,                  sinx*cosy,                  cosx*cosy, z],
                [        0,                          0,                          0, 1]])
print(r2)
basePos = r2.dot(r1.dot(camPos)) 
print(basePos)
for i in range(len(basePos)):
    basePos[i] = round(basePos[i],4)
print(basePos)
# %%
