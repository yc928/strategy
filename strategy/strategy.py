from strategy.strategyAPI import StrategyAPI
import time


class IMU():
    roll = 0.0
    pitch = 0.0
    yaw =0.0

class Ball():
    def __init__(self):
        self.detected = False
        
    def process(self, color_list):
        for i in range(len(color_list)):
            print('ball size: ', color_list[i].size)
            print('ball x: ', color_list[i].x)
            print('ball y: ', color_list[i].y)
            if color_list[i].size > 100:
                self.x = color_list[i].x
                self.y = color_list[i].y
                self.size = color_list[i].size
                self.detected = True
                
class Robot():
    def __init__(self):
        self.detected = False
        
    def process(self, red_list, blue_list):
        for i in range(len(red_list)):
            for j in range(len(blue_list)):
                if abs(red_list[i].ymax - blue_list[j].ymin) < 20:
                    print('robot')
                    self.x = red_list[i].x
                    self.detected = True
                else:
                    print('not robot')
            

class Strategy():

    def __init__(self):
        self.api = StrategyAPI()
        
        self.start = False
        self.init_flag = False

        self.head_init_flag = True
        self.sw1 = False
        self.sw2 = False
        self.sw3 = False
        self.forwardOK_flag = False
        self.turnOK_flag = False
        self.shiftOK_flag = False
        self.turnhead_flag = False
        self.kick_flag = False
        
        self.head_angle = 1700
        self.head_min_limit = 1300
        self.head_max_limit = 1900
    
    def main(self, object_info):
        ball = Ball()
        robot = Robot()
        
        #robot_flag = False
        if self.start:
            self.init_flag = True
            #self.api.sendbodyauto(2500, 0, 0, 0, 0x01, 0)
            #self.api.sendcontinuousvalue(1000, 0, 0, 0, 0)
            
            if self.head_init_flag:
                self.api.sendheadvalue(1, 50, 2048)
                self.api.sendheadvalue(2, 50, self.head_angle)
                self.head_init_flag = False

            #print(IMU.roll)
            #print(IMU.pitch)
            #print(IMU.yaw)
            #print('==============')
        #============goal keeper===================
            '''robot.process(object_info.colorobjects[5].objects, object_info.colorobjects[2].objects)
            ball.process(object_info.colorobjects[3].objects)
            
            if robot.detected and ball.detected:
                if robot.x - ball.x > 0:
                    print('ball at left')
                else:
                    print('ball at right')
            else:
                print('robot or ball missing')'''         
         
         #===========attacker=====================
            ball.process(object_info.colorobjects[3].objects)
            if ball.detected:
                if self.forwardOK_flag and self.turnOK_flag:
                    self.calc_shift(ball.x)
                    if self.kick_flag:
                        print('kick motion')
                        self.kick_flag = False
                        self.forwardOK_flag = False
                        self.turnOK_flag = False
                        self.shiftOK_flag = False
                        self.turnhead_flag = False
                        time.sleep(0.5)
                else:
                    self.calc_turn(ball.x)
                    self.calc_forward(ball.y)
                    self.calc_turnhead(ball.y)
               
            else:
                #goal keeper info
                self.head_angle = 1700
                self.head_init_flag = True
                                   
        else:
            self.head_init_flag = True
            self.turnhead_flag = False
            self.forwardOK_flag = False
            self.turnOK_flag = False
            self.shiftOK_flag = False
            self.turnhead_flag = False
            self.api.sendheadvalue(1, 50, 2048)
            self.api.sendheadvalue(2, 50, 2048)
            if self.init_flag:
                #self.api.sendbodyauto(0, 0, 0, 0, 0x01, 0)
                self.init_flag = False
            
    
    
    def calc_forward(self, ball_y):
        self.forwardOK_flag = False
        if ball_y < 40:
            print('go go go')
        elif ball_y < 80:
            print('go go')
        elif ball_y < 160:
            print('go')
        elif ball_y < 220:
            print('no go')
            if self.turnhead_flag:
                self.forwardOK_flag = True
        else:
            print('> 220')
            
    def calc_turn(self, ball_x):
        self.turnOK_flag = False
        if ball_x < 40:
            print('turn big left')
        elif ball_x < 120:
            print('turn left')
        elif ball_x < 200:
            print('no turn ')
            if self.turnhead_flag:
                self.turnOK_flag = True
        elif ball_x < 280:
            print('turn right')
        else:
            print('turn big right')
            
    def calc_shift(self, ball_x):
        self.shiftOK_flag = False
        if ball_x < 180:
            print('shift left')
        elif ball_x < 200:
            print('kick')
            self.kick_flag = True
        else:
            print('shift right')
        
    def calc_turnhead(self, ball_y):
        if ball_y < 100:
            self.head_angle = self.head_angle +10
        elif ball_y < 140:
            self.head_angle = self.head_angle
        else:
            self.head_angle = self.head_angle - 10
            
        if self.head_min_limit <= self.head_angle <= self.head_max_limit: 
            self.api.sendheadvalue(2, 50, self.head_angle)
        elif self.head_angle < self.head_min_limit:
            self.api.sendheadvalue(2, 50, self.head_min_limit)
            self.head_angle = self.head_min_limit
            self.turnhead_flag = True
        else: #head_angle > head_max_limit
            self.api.sendheadvalue(2, 50, self.head_max_limit)
            self.head_angle = self.head_max_limit
            
