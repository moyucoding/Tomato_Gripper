import pyzed.sl as sl
import time

class ZedHandler:
    def __init__(self) -> None:
        self.camera = sl.Camera()
        self.initPara = sl.InitParameters()
        self.initPara.camera_fps = 1
        self.initPara.camera_resolution = sl.RESOLUTION.HD2K
        #self.camera.open()
        self.calibration_parameters = self.camera.get_camera_information().calibration_parameters
        self.imgL = ''
        self.imgR = ''
        pass
    
    def open(self):
        if not self.camera.is_opened():
            print("Camera Opening")
            init = sl.InitParameters()
            err = self.camera.open(self.initPara)
            count = 1
            while err != sl.ERROR_CODE.SUCCESS:
                print("Camera Opening, retry:", count)
                err = self.camera.open(self.initPara)
                count += 1
                time.sleep(1)
            self.calibration_parameters = self.camera.get_camera_information().calibration_parameters
        print("Camera Opened.")
        pass

    def shoot(self):
        matL = sl.Mat()
        matR = sl.Mat()
        if self.camera.grab() == sl.ERROR_CODE.SUCCESS:
            self.camera.retrieve_image(matL, sl.VIEW.LEFT)
            self.camera.retrieve_image(matR, sl.VIEW.RIGHT)
            self.imgL = matL.get_data()[ : , : , :3]
            self.imgR = matR.get_data()[ : , : , :3]
        pass

    def close(self):
        self.camera.close()
        print("Camera closed.")