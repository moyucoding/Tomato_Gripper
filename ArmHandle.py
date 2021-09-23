import os
import socket
import time

class ArmHandler:
    def __init__(self, nterval, host, port, buf_size) -> None:
        self.interval = interval
        self.host = host
        self.port = port
        self.arm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.arm.connect((self.host, self.port))
        self.buf_size = buf_size

        self.request = ''
        self.result = ''

        try:
            os.mkfifo('/tmp/ArmControl1.pipe')
        except:
            pass
        try:
            os.mkfifo('/tmp/ArmControl2.pipe')
        except:
            pass
        
    
    def movePos(self, target):
        buf_size = 1024
        self.arm.send(bytes(target, 'utf-8'))
        print('[Info] Send movePos request to arm.') 
        #Get result
        time1 = time.time()
        result = self.arm.recv(buf_size)
        while not bool(result.decode('utf-8')):
            result = self.arm.recv(buf_size)
        time2 = time.time()
        print('[Info] Moving time:', time2 - time1, '.')
        

    def getPos(self):
        #Send msg
        self.arm.send(bytes('0', 'utf-8'))
        print('[Info] Send getPos request to arm.') 
        #Get result
        result = self.arm.recv(self.buf_size)
        #Result to string
        msg = str(result, 'utf-8')
        #Remove \x00
        msg = msg[:-3]
        pos = msg.split(',')
        for i in range(7):
            pos[i] = round(float(pos[i]), 2)
        str_pos = ','.join(str(num) for num in pos)
        return str_pos

    def holdGripper(self):
        #Send msg
        print('[Info] Send holdGripper request to arm.') 
        self.arm.send(bytes('3', 'utf-8'))
        time.sleep(0.5)
        pass

    def releaseGripper(self):
        #Send msg
        print('[Info] Send releaseGripper request to arm.')
        self.arm.send(bytes('4', 'utf-8'))
        time.sleep(0.5)
        pass

    def run(self):
        fd1 = os.open('/tmp/ArmControl1.pipe', os.O_CREAT | os.O_RDONLY)
        fd2 = os.open('/tmp/ArmControl2.pipe', os.O_SYNC | os.O_CREAT | os.O_WRONLY)
        while True:
            try:
                #Get request from PLC
                pipe_raw = os.read(fd1, 200)
                self.request = pipe_raw.decode('utf-8').split(';')
                if self.request[0] == 'movePos':
                    print('[Info] Get movePos request from PLC.')
                    #Send request to arm
                    target = self.request[1]
                    self.movePos(target)
                    #Send result to PLC
                    print('[Info] Get movePos result from arm.')
                    ret = 'Y;movePos;' + ' '*190
                    os.write(self.fd2, ret.encode('utf-8'))
                    print('[Info] Send movePos result to PLC')

                elif self.request[0] == 'getPos':
                    print('[Info] Get getPos request from PLC.')
                    #Send result to arm
                    pos = self.getPos()
                    #Send result to PLC
                    print('[Info] Get getPos result from arm.')
                    self.result = 'Y;getPos;' + pos + ';' +' '*(190 - len(pos))
                    os.write(self.fd2, self.result.encode('utf-8'))
                    print('[Info] Send getPos result to PLC')

                elif self.request[0] == 'holdGripper':
                    print('[Info] Get holdGripper request from PLC.')
                    #Send result to gripper
                    self.holdGripper()
                    #Send result to PLC
                    ret = 'Y;holdGripper;' + ' '*186
                    os.write(self.fd2, ret.encode('utf-8'))
                    print('[Info] Send holdGripper result to PLC')

                elif self.request[0] == 'releaseGripper':
                    print('[Info] Get releaseGripper request from PLC.')
                    #Send result to gripper
                    self.releaseGripper()
                    #Send result to PLC
                    ret = 'Y;releaseGripper;' + ' '*183
                    os.write(self.fd2, ret.encode('utf-8'))
                    print('[Info] Send releaseGripper result to PLC')
                
            except:
                print('[Error] ArmHandler.')
            time.sleep(self.interval/2)    

