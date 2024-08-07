import sys
sys.path.insert(0, "LeapLib/")
import math
import Leap, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pyduino import *
import numpy as np

class LeapMotionListener(Leap.Listener):
    
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        
        self.oldtime = time.time()
        self.newtime = time.time()
        
        self.a = Arduino(serial_port = 'COM3')

        self.motor7 = 7
        self.motor8 = 8
        self.motor9 = 9
        self.motor10 = 10
        self.motor11 = 11

        time.sleep(1)
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
    
    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
         
        self.a.motor_write(self.motor7, 180)
        self.a.motor_write(self.motor8, 180)
        self.a.motor_write(self.motor9, 0)
        self.a.motor_write(self.motor10, 40)
        self.a.motor_write(self.motor11, 130)     
        
        time.sleep(1)
        self.a.close()
        print "Exited"


    def on_frame(self, controller):
        
        frame = controller.frame()
        interaction_box = frame.interaction_box
        normalized_point = None

        for hand in frame.hands:
            
            handType = "Left hand" if hand.is_left else "Right hand"
            normalized_point = interaction_box.normalize_point(hand.palm_position, True)


            normal = hand.palm_normal
            direction = hand.direction

    
            Vector1_thump = hand.fingers[0].bone(2).direction
            Vector2_thump = hand.fingers[0].bone(3).direction
            Bda_thump = Vector1_thump.dot(Vector2_thump) * Leap.RAD_TO_DEG
            nor_thump = (Bda_thump-30)/20
            if nor_thump >= 1:
                nor_thump = 1
            if nor_thump <= 0:
                nor_thump = 0
            Thump_servo = math.floor(abs(130+nor_thump*50))
            self.a.motor_write(self.motor7, int(Thump_servo))
            #print Bda_thump
            print Thump_servo



            Vector1_index = hand.fingers[1].bone(0).direction
            Vector2_index = hand.fingers[1].bone(1).direction
            Bda_index = Vector1_index.dot(Vector2_index) * Leap.RAD_TO_DEG
            nor_index = (Bda_index-20)/35
            if nor_index >= 1:
                nor_index = 1
            if nor_index <= 0:
                nor_index = 0
            Index_servo = math.floor(abs(130+nor_index*50))
            #self.a.motor_write(self.motor8, int(Index_servo))
            #print Index_servo
            #print Bda_index


            Vector1_middle = hand.fingers[2].bone(0).direction
            Vector2_middle = hand.fingers[2].bone(1).direction
            Bda_middle = Vector1_middle.dot(Vector2_middle) * Leap.RAD_TO_DEG
            nor_middle = (Bda_middle-15)/30
            if nor_middle >= 1:
                nor_middle = 1
            if nor_middle <= 0:
                nor_middle = 0
            Middle_servo = math.floor(abs(70-nor_middle*70))
            #self.a.motor_write(self.motor9, int(Middle_servo))
            #print Middle_servo
            #print Bda_middle


            Vector1_ring = hand.fingers[3].bone(0).direction
            Vector2_ring = hand.fingers[3].bone(1).direction
            Bda_ring = Vector1_ring.dot(Vector2_ring) * Leap.RAD_TO_DEG
            nor_ring = (Bda_ring-20)/30
            if nor_ring >= 1:
                nor_ring = 1
            if nor_ring <= 0:
                nor_ring = 0
            Ring_servo = math.floor(abs(nor_ring*40))
            #self.a.motor_write(self.motor10, int(Ring_servo))
            #print Bda_ring
            #print Ring_servo


            Vector1_pinky = hand.fingers[4].bone(0).direction
            Vector2_pinky = hand.fingers[4].bone(1).direction
            Bda_pinky = Vector1_pinky.dot(Vector2_pinky) * Leap.RAD_TO_DEG
            nor_pinky = (Bda_pinky-25)/25
            if nor_pinky >= 1:
                nor_pinky = 1
            if nor_pinky <= 0:
                nor_pinky = 0
            Pinky_servo = math.floor(abs(180-nor_pinky*50))
            #self.a.motor_write(self.motor11, int(Pinky_servo))
            #print Bda_pinky
            #print Pinky_servo

            #print ' Thump: %s, Indez: %s, Middle: %s, Ring: %s, Pinky: %s ' % (Thump_servo, Index_servo, Middle_servo, Ring_servo, Pinky_servo)



def main():
    # Create a sample listener and controller
    listener = LeapMotionListener()
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