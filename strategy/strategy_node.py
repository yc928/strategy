import rclpy
import numpy as np
import time

from concurrent.futures import ThreadPoolExecutor
import os
from rclpy.node import Node
from rclpy.executors import Executor
from sensor_msgs.msg import Image

from std_msgs.msg import Bool
from std_msgs.msg import UInt8
from tku_msgs.msg import ColorObjects
from tku_msgs.msg import Interface
from tku_msgs.msg import DrawData

from strategy.strategy import Strategy
from strategy.imu_node import IMU_node

class StrategyComm(Node):
    def __init__(self):
        super().__init__('strategy_node')

        self.dio_sub = self.create_subscription(
                UInt8,
                '/package/FPGAack',
                self.dio_callback,
                10)
        self.dio_sub

        self.web_start_sub = self.create_subscription(
                Bool,
                '/web/start',
                self.web_start_callback,
                10)
        self.web_start_sub
                
        self.origin_image_sub = self.create_subscription(
                 Image,
                 '/ori_image',
                 self.origin_image_callback,
                 1)
        self.origin_image_sub
        
        self.colormodel_image_sub = self.create_subscription(
                 Image,
                 '/colormodel_image',
                 self.colormodel_image_callback,
                 1)
        self.colormodel_image_sub
        
        self.object_info_sub = self.create_subscription(
                 ColorObjects,
                 '/Object/List',
                 self.object_info_callback,
                 1)
        self.object_info_sub
              
        self.strategy = Strategy()
        
        self.strategy.api.sendbodyauto_pub = self.create_publisher(Interface, '/SendBodyAuto_Topic', 1)
        self.strategy.api.sendcontinuousvalue_pub = self.create_publisher(Interface, '/ChangeContinuousValue_Topic', 1)
        self.strategy.api.draw_pub = self.create_publisher(DrawData, '/draw_image', 1)
        


    def web_start_callback(self, msg):
        self.strategy.start = msg.data

    def dio_callback(self, msg):
        self.dio_data = msg.data
        
        self.strategy.start = bool(msg.data & 0x10)
        self.strategy.sw1 = bool(msg.data & 0x01)
        self.strategy.sw2 = bool(msg.data & 0x02)
        self.strategy.sw3 = bool(msg.data & 0x04)
        

        
      
    # image
    def origin_image_callback(self, msg):
        #print('origin_image_callback')
        pass
   
    def colormodel_image_callback(self, msg):
        print('colormodel_image_callback')
        
   
    def object_info_callback(self, msg):
        print('object_info_callback')
        self.strategy.main()
            
            
class PriorityExecutor(Executor):

    def __init__(self):
        super().__init__()
        self.high_priority_nodes = set()
        self.hp_executor = ThreadPoolExecutor(max_workers=os.cpu_count() or 4)
        self.lp_executor = ThreadPoolExecutor(max_workers=1)
        
    def add_high_priority_node(self, node):
        self.high_priority_nodes.add(node)
        # add_node inherited
        self.add_node(node)
        
    def spin_once(self, timeout_sec=None):
        # wait_for_ready_callbacks yields callbacks that are ready to be executed
        try:
            handler, group, node = self.wait_for_ready_callbacks(timeout_sec=timeout_sec)
        except StopIteration:
            pass
        else:
            if node in self.high_priority_nodes:
                self.hp_executor.submit(handler)
            else:
                self.lp_executor.submit(handler)
    

def main(args=None):
    rclpy.init(args=args)
    
    try:
        strategy_node = StrategyComm()
        imu_node = IMU_node()
        
        executor = PriorityExecutor()
        executor.add_high_priority_node(strategy_node)
        executor.add_node(imu_node)
        
        try:
            executor.spin()
        finally:
            executor.shutdown()
            strategy_node.destroy_node()
            imu_node.destroy_node()
    finally:
        rclpy.shutdown()
    '''strategy_node = StrategyComm()
    
    while rclpy.ok():
        print('in while')
        rclpy.spin_once(strategy_node)
        print('in while2')
        time.sleep(1)'''
        

    #rclpy.spin(strategy_node)

    #strategy_node.destroy_node()

    #rclpy.shutdown()


if __name__ == '__main__':
    main()
