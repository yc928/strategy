import rclpy
import time

from rclpy.node import Node
from tku_msgs.msg import SensorPackage
from strategy.strategy import IMU

class IMU_node(Node):
    def __init__(self):
        super().__init__('imu_node')
        
        self.imu_sub = self.create_subscription(
                 SensorPackage,
                 '/package/sensorpackage',
                 self.imu_callback,
                 1)
        self.imu_sub
        
         
    # imu
    def imu_callback(self, data):
        IMU.roll = data.imudata[0]
        IMU.pitch = data.imudata[1]
        IMU.yaw = data.imudata[2]
        #print(id(IMU))
        #print(IMU.roll)
        #print(IMU.pitch)
        #print(IMU.yaw)
        
    

def main(args=None):
    rclpy.init(args=args)

    imu_node = IMU_node()
    
    while rclpy.ok():
        rclpy.spin_once(imu_node)
        
    #rclpy.spin(imu_node)

    imu_node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
