import cv2
import pyzed.sl as sl

class ZedHandler:
    def __init__(self) -> None:
        self.camera = sl.Camera()
        self.calibration_parameters = self.camera.get_camera_information().calibration_parameters
        self.imgL = ''
        self.imgR = ''
        pass

    def shoot(self):
        matL = sl.Mat()
        matR = sl.Mat()
        
        self.imgL = matL.get_data()[ : , : , :3]
        self.imgR = matR.get_data()[ : , : , :3]
        
        pass