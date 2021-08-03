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

def main():
    arm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    arm.connect(('192.168.127.20', 5062))

    targets = ['219.91,-332.00,289.34,0.21,0.66,-0.65,0.32','636.63,138.27,410.64,0.12,-0.72,0.07,-0.68']
    for target in targets:
        movePos(arm, target, 1)

if __name__ == '__main__':
    main()