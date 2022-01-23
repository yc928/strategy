import rclpy
import numpy as np

from rclpy.node import Node

from std_msgs.msgs import Bool
from std_msgs.msgs import UInt8

class StrategyComm(node):
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
                '/web/stary',
                self.web_start_callback,
                10)
        self.web_start_sub

        self.strategy_start = False


    def web_start_callback(self, msg):
        self.web_start = msg.data

    def dio_callback(self, msg):
        self.dio_data = msg.data
        if msg.data & 0x10:
            self.web_start = True
        else:
            self.web_start = False  

def main(args=None):
    rclpy.init(args=args)

    strategy_node = StrategyComm()

    rclpy.spin(strategy_node)

    strategy_node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
