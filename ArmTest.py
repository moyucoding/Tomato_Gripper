import os
import socket
import time


def __init__(self, pipe_path, interval, host, port, buf_size) -> None:
        self.interval = interval
        self.pipe_path = pipe_path
        self.host = host
        self.port = port
        self.arm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.arm.connect((self.host, self.port))
        self.buf_size = buf_size

def movePos(arm, target, speed):
    buf_size = 1024
    #Target to string
    #target = '0,0,0,0,0,0,0'
    speed = 1
    #Send string
    arm.send(bytes(str(speed) + ',' + target, 'utf-8'))
    #Get result
    result = arm.recv(buf_size)
    while not bool(result.decode('utf-8')):
        result = arm.recv(buf_size)

def getPos(arm):
    buf_size = 1024
    arm.send(bytes('0', 'utf-8'))
    #Get result
    result = arm.recv(buf_size)
    print(result)
    #Result to string
    pos = '0,0,0,0,0,0,0'


def main():
    arm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    arm.connect(('192.168.127.20', 5062))

    '''
    targets = ['219.91,-332.00,289.34,0.21,0.66,-0.65,0.32','636.63,138.27,410.64,0.12,-0.72,0.07,-0.68']
    for target in targets:
        movePos(arm, target, 1)
    '''
    getPos(arm)

if __name__ == '__main__':
    main()

    '''
    b'636.47314453125,138.40185546875,410.58065795898,0.12007275223732,-0.71999657154083,0.069882988929749,-0.67992925643921\x00'
    '''
#%%
a = b'636.47314453125,138.40185546875,410.58065795898,0.12007275223732,-0.71999657154083,0.069882988929749,-0.67992925643921\x00'
print(type(a))
str_a = str(a, 'utf-8')
str_a = str_a[:-3]
print(str_a)
array_a = str_a.split(',')
print(array_a)
for i in range(7):
    array_a[i] = round(float(array_a[i]),2)
print(array_a)
str_a = ','.join(str(num) for num in array_a)
print(str_a)
# %%
