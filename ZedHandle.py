import pyzed.sl as sl
import time

class ZedHandler:
    def __init__(self) -> None:
        self.camera = sl.Camera()
        self.initPara = sl.InitParameters()
        self.initPara.camera_fps = 1
        self.initPara.camera_resolution = sl.RESOLUTION.HD2K
        #self.camera.open()
        self.runtime = sl.RuntimeParameters()
        self.calibration_parameters = self.camera.get_camera_information().calibration_parameters
        self.imgL = ''
        self.imgR = ''
        self.open()
        pass
    
    def open(self):
        if not self.camera.is_opened():
            print("Camera Opening")
            #init = sl.InitParameters()
            err = self.camera.open(self.initPara)
            count = 1
            while err != sl.ERROR_CODE.SUCCESS:
                print("Camera Opening, retry:", count)
                err = self.camera.open(self.initPara)
                count += 1
                time.sleep(1)
            self.calibration_parameters = self.camera.get_camera_information().calibration_parameters
        #print("Camera Opened.")
        pass

    def shoot(self):
        self.open()
        matL = sl.Mat()
        matR = sl.Mat()
        #print('Mat Created')
        if self.camera.grab(self.runtime) == sl.ERROR_CODE.SUCCESS:
            #print('Grabbed.')
            self.camera.retrieve_image(matL, sl.VIEW.LEFT)
            self.camera.retrieve_image(matR, sl.VIEW.RIGHT)
            #print('Retrieved images.')
            self.imgL = matL.get_data()[ : , : , :3]
            self.imgR = matR.get_data()[ : , : , :3]
            #print('Photo Shooted.')
        #self.close()
        pass

    def close(self):
        self.camera.close()
        print("Camera closed.")