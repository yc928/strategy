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
            #print('ball size: ', color_list[i].size)
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
        self.head_min_limit = 1450
        self.head_max_limit = 1900
        
        self.FORWARD_LARGE = 2000
        self.FORWARD_MEDIUM = 1500
        self.FORWARD_SMALL = 1000
        self.BACKWARD_SMALL = -800
        self.TURN_LLARGE = 10
        self.TURN_LSMALL = 5
        self.NO_TURN = 0
        self.TURN_RSMALL = -5
        self.TURN_RLARGE = -10
        self.SHIFT_LSMALL = 600
        self.SHIFT_RSMALL = -600
        self.WALKING_X_OFFSET = 0
        self.WALKING_Y_OFFSET = 0
        self.WALKING_THETA_OFFSET = 0
    
    def main(self, object_info):
        ball = Ball()
        robot = Robot()
        
        #robot_flag = False
        if self.start:
            if not self.init_flag:
                self.init_flag = True
                #self.api.sendbodyauto(self.WALKING_X_OFFSET, self.WALKING_Y_OFFSET, 0, self.WALKING_THETA_OFFSET, 0x01, 0)
                #self.api.sendsector(1)
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
                    #self.api.sendcontinuousvalue(self.WALKING_X_OFFSET, self.calc_shift(ball.x), 0, self.WALKING_THETA_OFFSET, 0)
                    self.calc_shift(ball.x)
                    if self.kick_flag:
                        print('kick motion')
                        self.kick_flag = False
                        self.forwardOK_flag = False
                        self.turnOK_flag = False
                        self.shiftOK_flag = False
                        self.turnhead_flag = False
                        time.sleep(10)
                else:
                    #self.api.sendcontinuousvalue(self.calc_forward(ball.y), self.WALKING_Y_OFFSET, 0, self.calc_turn(ball.x), 0)
                    self.calc_forward(ball.y)
                    self.calc_turn(ball.x)
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
            self.api.sendheadvalue(2, 50, 1700)
            if self.init_flag:
                #self.api.sendbodyauto(0, 0, 0, 0, 0x01, 0)
                #self.api.sendsector(2)
                self.init_flag = False
   
    def calc_forward(self, ball_y):
        self.forwardOK_flag = False
        if ball_y < 40:
            print('go go go')
            return self.FORWARD_LARGE
        elif 40 <= ball_y < 80:
            print('go go')
            return self.FORWARD_MEDIUM
        elif 80 <= ball_y < 190:
            print('go')
            return self.FORWARD_SMALL
        elif 190 <= ball_y < 220:
            print('no go')
            if self.turnhead_flag:
                self.forwardOK_flag = True
            return self.WALKING_X_OFFSET
        else:
            print('back back')
            return self.BACKWARD_SMALL
            
    def calc_turn(self, ball_x):
        self.turnOK_flag = False
        if ball_x < 40:
            print('turn big left')
            return self.TURN_LLARGE
        elif ball_x < 120:
            print('turn left')
            return self.TURN_LSMALL
        elif ball_x < 200:
            print('no turn ')
            if self.turnhead_flag:
                self.turnOK_flag = True
            return self.NO_TURN
        elif ball_x < 280:
            print('turn right')
            return self.TURN_RSMALL
        else:
            print('turn big right')
            return self.TURN_RLARGE
            
    def calc_shift(self, ball_x):
        self.shiftOK_flag = False
        if ball_x < 180:
            print('shift left')
            return self.SHIFT_LSMALL
        elif 180 <= ball_x < 200:
            print('kick')
            self.kick_flag = True
            return self.WALKING_Y_OFFSET
        else:
            print('shift right')
            return self.SHIFT_RSMALL
        
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
            
