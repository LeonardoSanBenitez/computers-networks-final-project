import serial
class Motor():
    def __init__(self):
        raise Exception('not implemented')

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

import serial
class MotorUART(Motor):
    '''
    @Brief: send to MSP430 via UART
    '''

    def __init__(self, debug=True):
        self._seq=0
        self._serial = serial.Serial("/dev/ttyS0", 115200, 
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE, 
                                    bytesize=serial.EIGHTBITS)
        if debug:
            import itertools 
            def test_gen():
                for i in itertools.cycle([0x80,0x81,0x82,0x83,0x84,0x00]): 
                    yield i
            self._gen = test_gen()

    def test_command(self, verbose=0):
        '''
        Return a valid command, iterating sequetially through all possible commands
        '''
        n = next(self._gen)
        if verbose: print('Send command', n)
        return n

    def send(self, command):
        '''
        Receives the hexadecimal command
        If read operation, return the value
        '''
        seq_low = (self._seq & 0x0F).to_bytes(1, 'big')
        seq_high = ((self._seq >> 8) & 0x0F).to_bytes(1, 'big')
        command = command.to_bytes(1, 'big')
        payload = seq_high + seq_low + command
        checksum = (sum(payload)%255).to_bytes(1, 'big')
        self._serial.write(seq_high + seq_low + command + checksum)

        self._seq = (self._seq + 1)%65535
        #if command==b'\x00':
        #    return self._serial.read(1)

