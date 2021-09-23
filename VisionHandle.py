import cv2
import numpy as np
import os
import time
import ZedHandle
import darknet

import logging
class YoloDetector:
    def __init__(self):
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        self.path = path + '/yolo'
        self.cfg = self.path + '/yolo-obj.cfg'
        self.data = self.path + '/obj.data'
        self.weight = self.path + '/yolo-obj_1.weights'
        self.batch_size = 1
        self.network, self.class_names, self.class_colors = darknet.load_network(self.cfg, self.data, self.weight, self.batch_size)
    
    def detect(self, img):
        #Image resize
        dark_h,dark_w = darknet.network_height(self.network), darknet.network_width(self.network)
        dark_img = darknet.make_image(dark_w, dark_h, 3)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized_img = cv2.resize(rgb_img, (dark_w, dark_h), interpolation = cv2.INTER_LINEAR)
        #YOLO detect tcp = (0.5,0,0.5,0,1.57,0)
        darknet.copy_image_from_bytes(dark_img, resized_img.tobytes())
        #cv2.waitKey()
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
        if not detections:
            return [0,0,0,(0,0,0,0,0)]

        return detections[0]

class VisionHandler:
    def __init__(self, interval) -> None:
        self.interval = interval
        
        self.camera = ZedHandle.ZedHandler()
        self.detetor = YoloDetector() 
        self.tcp = (0,0,0,0,0,0)

        self.imgL = ''
        self.imgR = ''
        self.objConf = 0
        self.objLabel = ''
        #objPix: x,y,w,h,d
        self.objPix = (0,0,0,0,0)
        self.objPos = (0,0,0,0,0,0)
        
        self.logfile = 'log.log'
        
        logging.basicConfig(level = logging.INFO, filename=self.logfile,filemode='a', format = '%(asctime)s - %(message)s')
        self.logger = logging.getLogger('vision')
        try:
            os.mkfifo('/tmp/Vision1.pipe')
        except:
            pass
        try:
            os.mkfifo('/tmp/Vision2.pipe')
        except:
            pass
        pass

    def takePhoto(self):
        time0 = time.time()
        #Take photo using API
        self.camera.shoot()
        #Set photo
        self.imgL = self.camera.imgL
        self.imgR = self.camera.imgR

        time1 = time.time()
        #print('Shoot:', time1-time0)
        self.logger.error('Shoot:' + str(time1-time0))
        pass

    def detectObject(self):
        time0 = time.time()
        #Target detection
        #Set objPix
        state, self.objLabel, self.objConf, self.objPix = self.detetor.detect(self.imgL)
        time1 = time.time()
        if state:
            ret = ''
            for p in self.objPix:
                ret += str(p)
                ret += ','
            self.logger.error(ret)
        else:
            self.logger.error('Detect Nothing.')
        self.logger.error('Detect:' + str(time1-time0))
        return bool(state) 
    
    def matchObject(self):
        time0 = time.time()
        #Load objPix
        x,y,w,h,_ = self.objPix

        cam_delta = self.camera.calibration_parameters.right_cam.cx - self.camera.calibration_parameters.left_cam.cx
        
        d = 0
        self.objPix = (x,y,w,h,d)

        #Matching between L/R pics
        half_w = w//2
        half_h = h//2
        meanDSR = 0.07076276 * (half_w * half_h) + 186.21035

        line = self.imgR[int(y - half_h): int(y + half_h), int(x - round(1.3 * meanDSR)) - int(half_w): int(x - round(0.8 * meanDSR) + half_w)]
        kernel_L = self.imgL[int(y - half_h): int(y + half_h), int(x - half_w): int(x + half_h)]
        cv2.imwrite('kl.jpg',kernel_L)
        try:
            matching = cv2.matchTemplate(line.copy(), kernel_L, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(matching)
            top_left = max_loc
        except:
            max_val = 0
        if max_val < 0.25:
            self.objPos = (0,0,0,0,0,0)
            time1 = time.time()
            self.logger.error('Match:' + str(time1 - time0))
            return False
        
        # Get distance
        d = - top_left[0] + round(1.3 * meanDSR)
        fx = self.camera.calibration_parameters.left_cam.fx
        b = self.camera.calibration_parameters.stereo_transform.m[0, 3]

        distance = fx * b / d
              
        self.objPos = (x,y,half_w,half_w,distance)
        pixX = x
        pixY = y

        camX = (pixX - self.camera.calibration_parameters.left_cam.cx) * distance / self.camera.calibration_parameters.left_cam.fx / 1000
        camY = (pixY - self.camera.calibration_parameters.left_cam.cy) * distance / self.camera.calibration_parameters.left_cam.fy / 1000
        camZ = distance / 1000
        self.objPos = (camX,  camY, camZ , 0, 0, 0)
        time1 = time.time()
        self.logger.error('Match:' + str(time1 - time0))
        return True

    def eyeToHand(self):
        camX, camY, camZ, _, _ ,_ =self.objPos
        camRx = 1.57
        camRy = 0
        camRz = 0
        self.objPos = (0.2+camZ,0-camX,0.4-camY, camRz, camRx, camRy)
        pass

    def eyeOnHand(self):
        #Get TCP
        #Rotation 1: Eye to TCP
        camX, camY, camZ, _, _, _ = self.objPos
        camPos = np.array([camX,camY,camZ,1])
        r1 = np.array([ [ 0,-1, 0, 0],
                        [ 0, 0,-1,10],
                        [ 1, 0, 0, 0],
                        [ 0, 0, 0, 1]])
        #Rotation 2: TCP to Base
        tcp = (0,0,0,0,0,0)
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
        
        basePos = camPos.dot(r1).dot(r2) 
        print(basePos)
        self.objPos = (basePos[0], basePos[1], basePos[2], 0,0,0)
        pass

    def getPos(self):
        
        if self.matchObject():
            #Eye to hand
            #self.eyeToHand()
            #Eye on hand
            self.eyeOnHand()
            return True
        return False

    def sendResult(self):
        pass

    def run(self):
        op_count = 0
        fd1 = os.open('/tmp/Vision1.pipe', os.O_CREAT | os.O_RDONLY)
        fd2 = os.open('/tmp/Vision2.pipe', os.O_SYNC | os.O_CREAT | os.O_WRONLY)
        while True:
            try:
                #Get request from PLC
                pipe_raw = os.read(fd1, 200)
                #pipe_raw = 'DetectObject;'
                self.request = pipe_raw.decode('utf-8').split(';')[0] 
                if self.request == 'DetectObject':
                    #Take photo
                    self.takePhoto()
                    #Detect object
                    if self.detectObject():
                        #Get position
                        if self.getPos():
                            #Send valid result to PLC
                            ret = []
                            #POS: m
                            for i in range(3):
                                tmp = str(round(self.objPos[i],4))
                                ret.append(tmp)
                            #ORI: rad
                            for i in range(3,6):
                                tmp = str(round(self.objPos[i],2))
                                ret.append(tmp)
                            ret = ','.join(ret)
                            ret = 'Y.DetectObject;' + ret + ';'
                        else:
                            ret = 'N.DetectObject;' + '0,0,0,0,0,0' + ';'
                    else:
                        ret = 'N.DetectObject;' + '0,0,0,0,0,0' + ';'

                    ret += ' '*(200 - len(ret))
                    os.write(fd2, ret.encode('utf-8'))
                    op_count += 1
                    self.logger.error('COUNT:' + str(op_count))
                    self.logger.error(ret)
                    print('Op:' + str(op_count))

                time.sleep(self.interval)
            except KeyboardInterrupt:
                break
        