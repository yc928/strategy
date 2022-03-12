from strategy.strategyAPI import StrategyAPI


class IMU():
    roll = 0.0
    pitch = 0.0
    yaw =0.0

    

class Strategy():

    def __init__(self):
        self.api = StrategyAPI()
        
        self.start = False
        self.init_flag = False
        self.sw1 = False
        self.sw2 = False
        self.sw3 = False
    
    def main(self):
        if self.start:
            #self.api.sendbodyauto(2500, 0, 0, 0, 0x01, 0)
            #self.api.sendcontinuousvalue(1000, 0, 0, 0, 0)
            self.init_flag = True
            print(IMU.roll)
            print(IMU.pitch)
            print(IMU.yaw)
            print('==============')            
        else:
        
            if self.init_flag:
                #self.api.sendbodyauto(0, 0, 0, 0, 0x01, 0)
                self.init_flag = False
            
    
    

