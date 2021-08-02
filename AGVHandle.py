import os
import serial
import struct
from threading import Thread
import time

class AGVHandler:
    def __init__(self, interval, pub_port, pub_rate, ctl_port, ctl_rate):
        self.interval = interval
        self.pub_port = pub_port
        self.pub_rate = pub_rate
        self.ctl_port = ctl_port
        self.ctl_rate = ctl_rate
        self.pos = [0,0,0]

        #Connect to serial
        self.publisher = serial.Serial(self.pub_port, self.pub_rate , timeout=2)
        self.pub_msg = ''
        self.controller = serial.Serial(self.ctl_port, self.ctl_rate, timeout=2)
        self.ctl_msg = ''

        #Initialize Decoder
        self.m1 = 0
        self.m2 = 0
        self.x_k1 = 0.00
        self.x_k11 = 0.00
        self.x_tR = 0.00
        self.x_k2 = 0.00
        self.x_k22 = 0.00
        self.x_tL = 0.00
        self.x_o = 0.00
        self.y_o = 0.00
        self.t_o = 0.00
        self.five = 0.00
        self.D = 0.162
        self.B = 0.460
        self.pi = 3.1415926

    def movePos(self, target):
        #Calculate the diff between current and target
        diff = [0,0]
        for i in range(0,2):
            diff[i] = target[i] - self.pos[i]
        #Encode msg
        self.ctl_msg = self.serialEncode(diff[0], diff[1])
        #Write msg to controller
        self.controller.write(self.ctl_msg)
        #Wait until AGV arrives
        while True:
            #Check the distance between current pos and target
            if self.pos == self.getPos():
                break

    def getPos(self):
        #Get msg from publisher
        self.pub_msg = self.publisher.read(64)
        #Decode msg
        self.pos = self.serialDecode()
        while not self.pos:
            self.serialDecode()

    def run(self):
        #Start publisher thread
        thread_publisher = Thread(target=self.getPos)
        thread_publisher.start()
        
        while True:
            #Get request from PLC
            pipe_raw = os.read(self.pipe, 200)
            self.request = pipe_raw.decode('utf-8').split(';')[0]
            self.request = ''
            if self.request == 'movePos':
                #Send request to arm
                target = ''
                speed = 1
                self.movePos(target, speed)
                #Send result to PLC
                os.write(self.pipe, 'Y.movePos'.encode('utf-8'))

            elif self.request == 'getPos':
                #Send result to arm
                self.getPos()
                ret = self.pos
                #Send result to PLC
                self.result = True
                os.write(self.pipe, 'Y.getPos'.encode('utf-8'))

            elif self.request[0] == 'y' or self.request[0] == 'n':
                #Resend to PLC 
                self.result = 1

            time.sleep(self.interval)


    def serialEncode(self,linear, angular):
        linear_sign = 0x00
        angular_sign = 0x00

        if linear < 0:
            linear_sign = 0x01
        if angular < 0 :
            angular_sign = 0x01
        
        data = struct.pack('>7B4h',0x01,0x10,0x10,0x51,0x00,0x04,0x08, linear, linear_sign, angular, angular_sign)
        crc_table=[0x0000,0xC0C1,0xC181,0x0140,0xC301,0x03C0,0x0280,0xC241,0xC601,0x06C0,0x0780,0xC741,0x0500,0xC5C1,0xC481,0x0440,0xCC01,0x0CC0,0x0D80,0xCD41,0x0F00,0xCFC1,0xCE81,0x0E40,0x0A00,0xCAC1,0xCB81,0x0B40,0xC901,0x09C0,0x0880,0xC841,0xD801,0x18C0,0x1980,0xD941,0x1B00,0xDBC1,0xDA81,0x1A40,0x1E00,0xDEC1,0xDF81,0x1F40,0xDD01,0x1DC0,0x1C80,0xDC41,0x1400,0xD4C1,0xD581,0x1540,0xD701,0x17C0,0x1680,0xD641,0xD201,0x12C0,0x1380,0xD341,0x1100,0xD1C1,0xD081,0x1040,0xF001,0x30C0,0x3180,0xF141,0x3300,0xF3C1,0xF281,0x3240,0x3600,0xF6C1,0xF781,0x3740,0xF501,0x35C0,0x3480,0xF441,0x3C00,0xFCC1,0xFD81,0x3D40,0xFF01,0x3FC0,0x3E80,0xFE41,0xFA01,0x3AC0,0x3B80,0xFB41,0x3900,0xF9C1,0xF881,0x3840,0x2800,0xE8C1,0xE981,0x2940,0xEB01,0x2BC0,0x2A80,0xEA41,0xEE01,0x2EC0,0x2F80,0xEF41,0x2D00,0xEDC1,0xEC81,0x2C40,0xE401,0x24C0,0x2580,0xE541,0x2700,0xE7C1,0xE681,0x2640,0x2200,0xE2C1,0xE381,0x2340,0xE101,0x21C0,0x2080,0xE041,0xA001,0x60C0,0x6180,0xA141,0x6300,0xA3C1,0xA281,0x6240,0x6600,0xA6C1,0xA781,0x6740,0xA501,0x65C0,0x6480,0xA441,0x6C00,0xACC1,0xAD81,0x6D40,0xAF01,0x6FC0,0x6E80,0xAE41,0xAA01,0x6AC0,0x6B80,0xAB41,0x6900,0xA9C1,0xA881,0x6840,0x7800,0xB8C1,0xB981,0x7940,0xBB01,0x7BC0,0x7A80,0xBA41,0xBE01,0x7EC0,0x7F80,0xBF41,0x7D00,0xBDC1,0xBC81,0x7C40,0xB401,0x74C0,0x7580,0xB541,0x7700,0xB7C1,0xB681,0x7640,0x7200,0xB2C1,0xB381,0x7340,0xB101,0x71C0,0x7080,0xB041,0x5000,0x90C1,0x9181,0x5140,0x9301,0x53C0,0x5280,0x9241,0x9601,0x56C0,0x5780,0x9741,0x5500,0x95C1,0x9481,0x5440,0x9C01,0x5CC0,0x5D80,0x9D41,0x5F00,0x9FC1,0x9E81,0x5E40,0x5A00,0x9AC1,0x9B81,0x5B40,0x9901,0x59C0,0x5880,0x9841,0x8801,0x48C0,0x4980,0x8941,0x4B00,0x8BC1,0x8A81,0x4A40,0x4E00,0x8EC1,0x8F81,0x4F40,0x8D01,0x4DC0,0x4C80,0x8C41,0x4400,0x84C1,0x8581,0x4540,0x8701,0x47C0,0x4680,0x8641,0x8201,0x42C0,0x4380,0x8341,0x4100,0x81C1,0x8081,0x4040]

        crc_hi=0xFF
        crc_lo=0xFF
        for w in data:
            index=crc_lo ^ ord(chr(w))
            crc_val=crc_table[index]
            crc_temp=crc_val//256
            crc_val_low=crc_val-(crc_temp*256)
            crc_lo=crc_val_low ^ crc_hi
            crc_hi=crc_temp
        crc=crc_hi*256 +crc_lo
        crc_hi = crc//256
        crc_lo = crc & 0xFF

        datalist = list(data)
        for i in range(len(datalist)):
            datalist[i] = chr(datalist[i])
        data = ''.join(datalist)
        return data+chr(crc_lo)+chr(crc_hi)

    def serialDecode(self):
        num = self.pub_msg.find('\x01\x02')
        num2 = num + 13
        if num == 0 or num > 0:
            b1, b2, b31, b32, b33, b34, b41, b42, b43, b44, b5, b6, b7 = struct.unpack('>13B',self.pub_msg[num:num2])
            return False
        if b5 != 0x0F or b1 != 0x01 or b2 != 0x02:
            self.pub_msg = self.publisher.read(1024)
            self.pub_msg = ' '
            return False
        else:
            if b31 > 127:  # b31 unsigned char
                b31 = 255 - b31
                b32 = 255 - b32
                b33 = 255 - b33
                b34 = 255 - b34 + 1
                self.x_k1 = -(b34 + b33 * 256 + b32 * 65536 + b31 * 16777216)
                if self.m1 == 0 or abs(self.x_k1 - self.x_k11) > 100000000:
                    self.x_tL = 0
                    self.m1 = 1
                else:
                    self.x_tL = self.x_k1 - self.x_k11
                    if abs(self.x_tL) < 10:
                        self.x_tL = 0

                self.x_k11 = self.x_k1
                
            elif b31 < 127 or b31 == 127:
                self.x_k1 = (b34 + b33 * 256 + b32 * 65536 + b31 * 16777216)
                if self.m1 == 0 or abs(self.x_k1 - self.x_k11) > 100000000:
                    self.x_tL = 0
                    self.m1 = 1
                else:
                    self.x_tL = self.x_k1 - self.x_k11
                    if abs(self.x_tL) < 10:
                        self.x_tL = 0
                    
                self.x_k11 = self.x_k1
                
            if b41 > 127:
                b41 = 255 - b41
                b42 = 255 - b42
                b43 = 255 - b43
                b44 = 255 - b44 + 1
                self.x_k2 = -(b44 + b43 * 256 + b42 * 65536 + b41 * 16777216)

                if self.m2 == 0 or abs(self.x_k2 - self.x_k22) > 100000000:
                    self.x_tR = 0
                    self.m2 = 1
                else:
                    self.x_tR = self.x_k2 - self.x_k22
                    if abs(self.x_tR) < 10:
                        self.x_tR = 0
                    
                self.x_k22 = self.x_k2

            elif b41 < 127 or b41 == 127:
                self.x_k2 = (b44 + b43 * 256 + b42 * 65536 + b41 * 16777216)
                if self.m2 == 0 or abs(self.x_k2 - self.x_k22) > 100000000:
                    self.x_tR = 0
                    self.m2 = 1
                else:
                    self.x_tR = self.x_k2 - self.x_k22
                    if abs(self.x_tR) < 10:
                        self.x_tR = 0

                self.x_k22 = self.x_k2
                
            self.five = self.five + self.D * self.pi * (self.x_tR // 25 - self.x_tL // 25) // (self.B * 10000) / 1.2333
            self.x_o = self.x_o + self.pi * self.D * (self.x_tR // 25 + self.x_tL // 25) * math.cos(self.five) / (10000 * 2) * 0.8194
            self.y_o = self.y_o + self.pi * self.D * (self.x_tR // 25 + self.x_tL // 25) * math.sin(self.five) / (10000 * 2) * 0.8194
            
            x = self.x_o
            y = self.y_o
            theta = self.five

            while theta > 3.1415926:
                theta -= 2 * 3.1415926
            while theta < -3.1415926:
                theta += 2 * 3.1415926
            self.pos =  [x,y,theta]