import cv2
import numpy as np
import os
import time
import ZedHandle
import darknet
class YoloDetector:
    def __init__(self):
        self.path = ''
        self.cfg = self.path + '/yolo-obj.cfg',
        self.data = self.path + '/obj.data',
        self.weight = self.path + '/yolo-obj_1.weights'
        self.batch_size = 1
        self.network, self.class_names, self.class_colors = darknet.load_network(self.cfg, self.data, self.weight, self.batch_size)
    
    def detect(self, img):
        #Image resize
        dark_h,dark_w = darknet.network_height(self.network), darknet.network_width(self.network)
        dark_img = darknet.make_image(dark_w, dark_h, 3)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized_img = cv2.resize(rgb_img, (dark_w, dark_h), interpolation = cv2.INTER_LINEAR)
        #YOLO detect
        darknet.copy_image_from_bytes(dark_img, resized_img.tobytes())
        cv2.waitKey()
        dark_detections = darknet.detect_image(self.network, self.class_names, dark_img, thresh = 0.4)
        darknet.free_image(dark_img)
        #Detection resize
        img_h,img_w = img.shape[:2]
        detections = []
        for d in dark_detections:
            label, conf, (x,y,w,h) = d
            x = x * img_w // dark_w 
            y = y * img_h // dark_h
            w = w * img_w // dark_w
            h = h * img_h // dark_h

            if x < 0:
                x = 0
            if x + w > img_w:
                w = img_w - x
            if y < 0 :
                y = 0
            if y + h > img_h:
                h = img_h - y
            
            detections.append((w*h, label, conf, (x,y,w,h,0)))
        #Sort detections
        detections.sort(key = lambda t:t[0], reverse=True)
        return detections[0]

class VisionHandler:
    def __init__(self, interval, vision_pipe_path) -> None:
        self.interval = interval
        self.pipe_path = vision_pipe_path
        self.camera = ZedHandle.ZedHandler()
        self.detetor = YoloDetector()

        self.imgL = ''
        self.imgR = ''
        self.objConf = 0
        self.objLabel = ''
        #objPix: x,y,w,h,d
        self.objPix = (0,0,0,0,0)
        self.objPos = (0,0,0,0,0,0)
        
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info] VisionHandler: Pipe: ',self.pipe_path,' exists.')
        self.pipe = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        pass

    def takePhoto(self):
        #Take photo using API
        self.camera.shoot()
        #Set photo
        self.imgL = self.camera.imgL
        self.imgR = self.camera.imgR
        pass

    def detectObject(self):
        #Target detection
        #Set objPix
        _, self.objLabel, self.objConf, self.objPix = self.detetor.detect(self.imgL)
        pass

    def filter(self, img):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
        return cv2.filter2D(img, -1, kernel=kernel)

    def getPos(self):
        #Load objPix
        #filtered_imgL = self.filter(self.imgL)
        #filtered_imgR = self.filter(self.imgR)
        #Template matching
        x,y,w,h,_ = self.objPix

        cam_delta = self.camera.calibration_parameters.right_cam.cx - self.camera.calibration_parameters.left_cam.cx
        
        d = 0
        self.objPix = (x,y,w,h,d)
        #Matrix operations
        half_w = w//2
        half_h = h//2
        value = -1

        meanDSR = 0.07076276 * (half_w * half_h) + 186.21035

        line = self.imgR[y - half_h: y + half_h, x - round(1.3 * meanDSR) - half_w: x - round(0.8 * meanDSR) + half_w]
        kernel_L = self.imgL[y - half_h:y + half_h, x - half_w:x + half_h]

        matching = cv2.matchTemplate(line.copy(), kernel_L, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matching)
        top_left = max_loc
        if max_val < 0.25:
            return
        
        d = - top_left[0] + round(1.3 * meanDSR)
        fx = self.camera.calibration_parameters.left_cam.fx
        b = self.camera.calibration_parameters.stereo_transform.m[0, 3]
        distance = fx * b / d

        self.objPos = (x,y,half_w,half_w,distance)
        pixX = x + w
        pixY = y + h
        pixZ = d

        camX = (pixX - self.camera.calibration_parameters.left_cam.cx) * pixZ / self.camera.calibration_parameters.left_cam.fx
        camY = (pixY - self.camera.calibration_parameters.left_cam.cy) * pixY / self.camera.calibration_parameters.left_cam.fy
        camZ = pixZ

        camRx = 0
        camRy = 0
        camRz = 0
        
        self.objPos = (camX, camY, camZ, camRx, camRy, camRz)

    def run(self):
        while True:
            #Get request from PLC
            pipe_raw = os.read(self.pipe, 200)
            #pipe_raw = 'DetectObject;'
            self.request = pipe_raw.decode('utf-8').split(';')[0] 
            if self.request == 'DetectObject':
                #Take photo
                self.takePhoto()
                #Detect object
                self.detectObject()
                #Get position
                self.getPos()
                #Send result to PLC
                os.write(self.pipe, 'Y.DetectObject'.encode('utf-8'))

            time.sleep(self.interval)