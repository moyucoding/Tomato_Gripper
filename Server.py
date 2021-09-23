from threading import Thread

#import ArmHandle
#import AGVHandle
import VisionHandle

def main(interval):

    #Initialize ArmHandler
    arm_host = '192.168.127.20'
    arm_port = 5062
    arm_buf_size = 1024

 #   arm_handler = ArmHandle.ArmHandler(interval, arm_host, arm_port, arm_buf_size)
 #   thread_arm_handler = Thread(arm_handler.run())
 #   thread_arm_handler.start()
    '''
    #Initialize AGVHandler
    agv_pub_port = '/dev/usb-232'
    agv_pub_rate = 115200
    agv_ctl_port = '/dev/usb-485'
    agv_ctl_rate = 38400
    agv_pipe_path = '/tmp/AgvControl.pipe'

    agv_handler = AGVHandle.AGVHandler(interval, agv_pipe_path, agv_pub_port, agv_pub_rate, agv_ctl_port, agv_ctl_rate)
    thread_agv_handler = Thread(agv_handler.run())
    thread_agv_handler.start()
    '''
    #Initialize VisionHandler
    vision_pipe_path = '/tmp/Vision.pipe'

    vision_handler = VisionHandle.VisionHandler(interval)
    thread_vision_handler = Thread(vision_handler.run())
    thread_vision_handler.start()
    

if __name__ == '__main__':
    plc_interval = 0.02
    main(plc_interval)