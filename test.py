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

vision.detectObject()
vision.getPos()
print(vision.objPos)