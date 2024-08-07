from pyduino import *
import time

if __name__ == '__main__':
    
    # if your arduino was running on a serial port other than '/dev/ttyACM0/'
    # declare: a = Arduino(serial_port='/dev/tty')
    a = Arduino(serial_port='COM5')    
    # sleep to ensure ample time for computer to make serial connection 
    time.sleep(3)    

    # declare the pin our servo is attached to
    # make sure this matches line 26 of one_servo.ino
    # the line that says: int SERVO2_PIN = 2;
    PIN = 1        
    a.set_pin_mode(PIN,'0')
    
    for i in range(0,1000):
        if i%2 == 0:
            print '45'
            # move servo on pin to an angle of 170 deg
            a.motor_write(PIN,0) 
        else:
            print '180'
                # move servo on pin to an angle of 10 deg
            a.motor_write(PIN,180) 

        time.sleep(1)
