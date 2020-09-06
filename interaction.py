class LED():
    def __init__(self, pin=16)
    self._pin = 16
    #TODO
    pass


class Motor():
    def __init__(self):
        pass

    def move(self, speed):
        '''
        Brief: Receve an speed, from -1 to 1
        Return: nothing
        '''
        pass

    def turn(self, angle):
        '''
        Receive an angle to turn, from -180 to 180
        angle=0 keep in the same direction
        '''
        pass


class MotorUART(Motor):
    '''
    @Brief: send to MSP430 via UART
    TODO
    '''

    def __init__(self):
        pass

    def move(self, speed):
        if speed > 0:
            pass
            # PWM1_DIR = foward
            # PWM1=speed

            # PWM2_DIR = foward
            # PWM2=speed
        elif speed < 0:
            pass
            # PWM1_DIR = backward
            # PWM1=speed

            # PWM2_DIR = backward
            # PWM2=speed
        else:
            pass
            # PWM1=0
            # PWM2=0

    def turn(self, angle):
        if angle > 0:
            pass  # PWM1_DIR = foward
            # PWM1=255
            # PWM2_DIR = backward
            # PWM2=255
            # wait xxx time (heuristic)
            # PWM1=0
            # PWM2=0
        elif angle < 0:
            pass
