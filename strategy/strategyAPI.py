import rclpy

from tku_msgs.msg import Interface
from tku_msgs.msg import DrawData
from tku_msgs.msg import HeadPackage

from tku_msgs.srv import ExecuteSector

class StrategyAPI():
    
    def __init__(self):      
        #self.sendbodyauto_pub = self.create_publisher(Interface, '/SendBodyAuto_Topic', 1)
        #self.sendcontinuousvalue_pub = self.create_publisher(Interface, '/ChangeContinuousValue_Topic', 1)
        #self.draw_pub = self.create_publisher(DrawData, '/draw_image', 1)
        pass
        
    def sendbodyauto(self, x, y, z, theta, walking_mode, sensor_mode):
        data = Interface()
        data.x = x
        data.y = y
        data.z = z
        data.theta = theta
        data.walking_mode = walking_mode
        data.sensor_mode = sensor_mode
        self.sendbodyauto_pub.publish(data)
        
    def sendcontinuousvalue(self, x, y, z, theta, sensor_mode):
        data = Interface()
        data.x = x
        data.y = y
        data.z = z
        data.theta = theta
        data.sensor_mode = sensor_mode
        self.sendcontinuousvalue_pub.publish(data)
        
    def sendheadvalue(self, head_id, speed, angle):
        data = HeadPackage()
        data.id = head_id
        data.position = angle
        data.speed = speed
        self.head_pub.publish(data)
        
    def sendsector(self, sector_id):
        data = ExecuteSector.Request()
        data.sector = sector_id
        self.sendsector_cli.call_async(data)
        
    def draw(self, draw_type, xmin, xmax, ymin, ymax, red, green, blue, width):
        data = DrawData()
        data.draw_type = draw_type
        data.xmin = xmin
        data.xmax = xmax
        data.ymin = ymin
        data.ymax = ymax
        data.red = red
        data.green = green
        data.blue = blue
        data.width = width
        self.draw_pub.publish(data)
        
        


 

