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
        
        self.a = Arduino(serial_port = 'COM10')

        self.motor1 = 1
        self.motor2 = 2
        self.motor3 = 3
        self.motor4 = 4
        self.motor5 = 5
        self.motor6 = 6
        self.motor7 = 7
        self.motor8 = 8
        self.motor9 = 9
        self.motor10 = 10
        self.motor11 = 11

        time.sleep(7)
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
         
        self.a.motor_write(self.motor2, -2500)
        self.a.motor_write(self.motor4, 0)
        self.a.motor_write(self.motor5, 400)
        self.a.motor_write(self.motor6, 90)
        self.a.motor_write(self.motor3, 2500)
        self.a.motor_write(self.motor1, -4000)
        self.a.motor_write(self.motor7, 180)
        self.a.motor_write(self.motor8, 180)
        self.a.motor_write(self.motor9, 0)
        self.a.motor_write(self.motor10, 40)
        self.a.motor_write(self.motor11, 130)     
        
        time.sleep(7)
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

            Pitch = direction.pitch * Leap.RAD_TO_DEG
            Pitch_ang = 75-Pitch
            if Pitch_ang >= 162:
                Pitch_ang = 162
            if Pitch_ang <= 0:
                Pitch_ang = 0
            Pitch_servo = math.floor(Pitch_ang*350/81)
            self.a.motor_write(self.motor5, int(Pitch_servo))


            Yaw   = direction.yaw   * Leap.RAD_TO_DEG
            Yaw_ang = 40-Yaw
            if Yaw_ang >= 95:
                Yaw_ang = 95
            if Yaw_ang <= 0:
                Yaw_ang = 0
            Yaw_servo = math.floor(150-Yaw_ang)
            self.a.motor_write(self.motor6, int(Yaw_servo))

    
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



            Vector1_index = hand.fingers[1].bone(0).direction
            Vector2_index = hand.fingers[1].bone(1).direction
            Bda_index = Vector1_index.dot(Vector2_index) * Leap.RAD_TO_DEG
            nor_index = (Bda_index-20)/35
            if nor_index >= 1:
                nor_index = 1
            if nor_index <= 0:
                nor_index = 0
            Index_servo = math.floor(abs(130+nor_index*50))
            self.a.motor_write(self.motor8, int(Index_servo))


            Vector1_middle = hand.fingers[2].bone(0).direction
            Vector2_middle = hand.fingers[2].bone(1).direction
            Bda_middle = Vector1_middle.dot(Vector2_middle) * Leap.RAD_TO_DEG
            nor_middle = (Bda_middle-15)/30
            if nor_middle >= 1:
                nor_middle = 1
            if nor_middle <= 0:
                nor_middle = 0
            Middle_servo = math.floor(abs(70-nor_middle*70))
            self.a.motor_write(self.motor9, int(Middle_servo))


            Vector1_ring = hand.fingers[3].bone(0).direction
            Vector2_ring = hand.fingers[3].bone(1).direction
            Bda_ring = Vector1_ring.dot(Vector2_ring) * Leap.RAD_TO_DEG
            nor_ring = (Bda_ring-20)/30
            if nor_ring >= 1:
                nor_ring = 1
            if nor_ring <= 0:
                nor_ring = 0
            Ring_servo = math.floor(abs(nor_ring*40))
            self.a.motor_write(self.motor10, int(Ring_servo))


            Vector1_pinky = hand.fingers[4].bone(0).direction
            Vector2_pinky = hand.fingers[4].bone(1).direction
            Bda_pinky = Vector1_pinky.dot(Vector2_pinky) * Leap.RAD_TO_DEG
            nor_pinky = (Bda_pinky-25)/25
            if nor_pinky >= 1:
                nor_pinky = 1
            if nor_pinky <= 0:
                nor_pinky = 0
            Pinky_servo = math.floor(abs(180-nor_pinky*50))
            self.a.motor_write(self.motor11, int(Pinky_servo))


            print ' Pitch: %s, Yaw: %s ' % ( Pitch_servo, Yaw_servo)
            print ' Thump: %s, Indez: %s, Middle: %s, Ring: %s, Pinky: %s ' % (Thump_servo, Index_servo, Middle_servo, Ring_servo, Pinky_servo)



        self.newtime = time.time()
        delta_time =  self.newtime - self.oldtime


        if delta_time > 0.4:

            frame = controller.frame()
            interaction_box = frame.interaction_box
            normalized_point = None

            for hand in frame.hands:
            
                handType = "Left hand" if hand.is_left else "Right hand"
                normalized_point = interaction_box.normalize_point(hand.palm_position, True)
                
                normal = hand.palm_normal
                direction = hand.direction

                self.XPOS = normalized_point.x
                self.YPOS = normalized_point.y
                self.ZPOS = normalized_point.z

                XPOS_stepper = self.XPOS*8000-4000 #self.XPOS*8000-4000
                YPOS_stepper = 1000- self.YPOS*1000 #2500-self.YPOS*2500
                ZPOS_stepper = self.ZPOS*4000-3300 #self.ZPOS*5000-3300
                
                Roll = normal.roll * Leap.RAD_TO_DEG
                if Roll >= 70:
                    Roll = 70
                if Roll <= -150:
                    Roll = -150
                Roll_stepper = math.floor(Roll*10)

                #self.a.motor_write(self.motor1,int(XPOS_stepper))
                #self.a.motor_write(self.motor2,int(YPOS_stepper))
                #self.a.motor_write(self.motor3,int(ZPOS_stepper))
                #self.a.motor_write(self.motor4, Roll_stepper)

                
                print 'X: ' + str(XPOS_stepper)
                print 'Y: ' + str(YPOS_stepper)
                print 'Z: ' + str(ZPOS_stepper)
                print 'Roll: %s ' % (Roll_stepper)
                
                self.oldtime = self.newtime

                
        else:
            pass

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