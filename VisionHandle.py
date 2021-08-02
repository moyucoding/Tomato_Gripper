import os
import time

class VisionHandler:
    def __init__(self, interval, vision_pipe_path) -> None:
        self.interval = interval
        self.pipe_path = vision_pipe_path
        self.camera = ''
        self.detetor = ''

        self.image = ''
        self.objPix = ''
        self.objPos = ''

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info] VisionHandler: Pipe: ',self.pipe_path,' exists.')
        self.pipe = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        #Initilize camera
        #Load detector

    def takePhoto(self):
        #Take photo using API
        #Set photo
        self.image = ''
        pass

    def detectObject(self):
        #Target detection
        #Set objPix
        self.objPix = ''
        pass

    def getPos(self):
        #Load objPix
        #Matrix operations
        self.objPos = ''
        pass

    def run(self):
        while True:
            #Get request from PLC
            pipe_raw = os.read(self.pipe, 200)
            self.request = pipe_raw.decode('utf-8').split(';')[0]
            self.request = ''
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