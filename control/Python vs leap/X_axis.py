import sys
sys.path.insert(0, "LeapLib/")
import math
import Leap, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pyduino import *
import numpy as np

class SampleListener(Leap.Listener):
    def on_init(self,controller):

     self.oldtime = time.time()
     self.newtime = time.time()
     
     self.motor4 =  1
     self.a = Arduino(serial_port='COM6')

    time.sleep(3)
    print "Initialized"


    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        
        self.a.motor_write(self.motor4, -4000) 
        time .sleep(3)
        self.a.close()

        print "Exited"

    def on_frame(self, controller):

        self.newtime = time.time()
        

        g = self.newtime-self.oldtime
        self.oldtime = self.newtime
        print g
        if self.newtime-self.oldtime > 0.7: # if difference between times is 10ms

            frame = controller.frame()
            interaction_box = frame.interaction_box
            normalized_point = None
           
            for hand in frame.hands:

                handType = "Left hand" if hand.is_left else "Right hand"
                normalized_point = interaction_box.normalize_point(hand.palm_position,True)

                self.XPOS = normalized_point.x

                XPOS_stepper = self.XPOS*10200-5200

                self.a.motor_write(self.motor4,int(XPOS_stepper)) # Azimuth

                print XPOS_stepper

                self.oldtime = self.newtime


        


        else:
            pass

def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()