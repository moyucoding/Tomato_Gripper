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
        #YOLO detect
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

        self.state = 0
        
        self.logfile = 'log.log'
        
        logging.basicConfig(level = logging.INFO, filename=self.logfile,filemode='a', format = '%(asctime)s - %(message)s')
        self.logger = logging.getLogger('vision')
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
        self.state, self.objLabel, self.objConf, self.objPix = self.detetor.detect(self.imgL)
        if self.state:
            self.state = 1
        pass

    def filter(self, img):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
        return cv2.filter2D(img, -1, kernel=kernel)

    def getPos(self):
        if not self.state:
            self.objPos = (0.5,0,0,0,1.57,0)
            return
        #Load objPix
        #filtered_imgL = self.filter(self.imgL)
        #filtered_imgR = self.filter(self.imgR)
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
            self.objPos = (0.5,0,0,0,1.57,0)
            return
        
        # Get distance
        d = - top_left[0] + round(1.3 * meanDSR)
        fx = self.camera.calibration_parameters.left_cam.fx
        b = self.camera.calibration_parameters.stereo_transform.m[0, 3]

        #fx = 1048.015625
        #b = 119.87950134277344
        distance = fx * b / d
        
        #newR = cv2.rectangle(self.imgR.copy(),(int(x-d-half_w//2), int(y-half_h//2)), (int(x-d+half_w//2),int(y+half_h//2)), (0,0,0), 2)
        #cv2.rectangle(self.imgR.copy(),(0,0), (100,100), (0,0,0), -1)
        #cv2.imwrite('r.jpg',newR)
        newL = cv2.rectangle(self.imgL.copy(), (int(x-half_w), int(y-half_h)), (int(x+half_w), int(y+half_h)), (218,165,0), 1)
        newR = cv2.rectangle(self.imgR.copy(),(int(x-d-half_w), int(y-half_h)), (int(x-d+half_w),int(y+half_h)), (218,165,0), 1)
        newRet = np.concatenate((newL,newR), axis=1)
        cv2.imwrite('match.jpg', newRet)
        self.objPos = (x,y,half_w,half_w,distance)
        pixX = x
        pixY = y

        #self.camera.calibration_parameters.left_cam.cx = 1115.858642578125
        #self.camera.calibration_parameters.left_cam.cy = 641.80859375
        #self.camera.calibration_parameters.left_cam.fx = 1048.015625
        #self.camera.calibration_parameters.left_cam.fy = 1048.015625

        camX = (pixX - self.camera.calibration_parameters.left_cam.cx) * distance / self.camera.calibration_parameters.left_cam.fx / 1000
        camY = (pixY - self.camera.calibration_parameters.left_cam.cy) * distance / self.camera.calibration_parameters.left_cam.fy / 1000
        camZ = distance / 1000

        camRx = 1.57
        camRy = 0
        camRz = 0


        self.objPos = (0.2+camZ,0-camX,0.4-camY, camRz, camRx, camRy)
        print('POS:',0.2+camZ,0-camX,0.4-camY)

    def run(self):
        op_count = 0
        resend_count = 0
        while True:
            try:
                #Get request from PLC
                pipe_raw = os.read(self.pipe, 200)
                #pipe_raw = 'DetectObject;'
                self.request = pipe_raw.decode('utf-8').split(';')[0] 
                if self.request == 'DetectObject':
                    #Take photo
                    time0 = time.time()
                    self.takePhoto()
                    time1 = time.time()
                    #print('Shoot:', time1-time0)
                    self.logger.error('Shoot:' + str(time1-time0))
                    #Detect object
                    self.detectObject()
                    time2 = time.time()
                    #print('Detect:', time2-time1)
                    ret = ''
                    for p in self.objPix:
                        ret += str(p)
                        ret += ','
                    self.logger.error(ret)
                    self.logger.error('Detect:' + str(time2-time1))
                    #Get position
                    self.getPos()
                    time3 = time.time()
                    #print('Match:',time3 - time2)
                    self.logger.error('Match:' + str(time3 - time2))
                    #Send result to PLC
                    ret = []
                    #POS: m
                    for i in range(3):
                        tmp = str(round(self.objPos[i],4))
                        ret.append(tmp)
                    #ORI: rad
                    for i in range(3,6):
                        tmp = str(round(self.objPos[i],2))
                        ret.append(tmp)
                    #ret = [str(round(i,2)) for i in self.objPos]
                    ret = ','.join(ret)
                    if (not self.state) or (ret == '0.5,0,0,0,1.57,0'):
                        ret = 'N.DetectObject;' + ret + ';'
                    else:
                        ret = 'Y.DetectObject;' + ret + ';'
                    ret += ' '*(200 - len(ret))
                    os.write(self.pipe, ret.encode('utf-8'))
                    op_count += 1
                    resend_count = 0
                    self.logger.error('COUNT:' + str(op_count))
                    self.logger.error(ret)
                    print('Op:' + str(op_count))
                    #print(ret)
                elif self.request[0] == 'Y' or self.request[0] == 'N':
                    os.write(self.pipe, pipe_raw)
                    resend_count += 1
                    self.logger.error('RESEND:' + str(resend_count))
                    self.logger.error(self.request)
                    time.sleep(self.interval/2)

                time.sleep(self.interval)
            except KeyboardInterrupt:
                break
            
            except:
                self.camera.close()
                print('Error. restarting')
                self.logger.error('RESTART')
            
        