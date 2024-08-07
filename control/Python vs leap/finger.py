# -*- coding: utf-8 -*-
import Leap, sys, thread, time
#import các loại cử chỉ
import numpy.linalg as la
import numpy as np
import math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#cài đặt nhận data từ leap

class LeapMotionListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'] #ngón tay
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal'] #xương bàn tay
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END'] #trạng thái
	oldtime = time.time()
	newtime = time.time()
	def on_init(seft, controller):
		print("Initialized")
	def on_connect(self, controller):
		print("Motion Sensor Connected") #đã kết nối cảm biến

		#cho phép cảm biến nhận cử chỉ
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print("Motion Sensor Disconnected") #đã ngắt kết nối
	def on_exit(self, controller):
		print("Exited") #đã thoát
	def on_frame(self, controller): #khung hình
		self.newtime = time.time()
		if self.newtime - self.oldtime > 0.2 :
			frame = controller.frame()
			for hand in frame.hands:


				for finger in hand.fingers:
					#CÁCH MỘT: DISTION TIP VS JOINT
					'''x1 = hand.fingers[1].bone(0).next_joint[0]
					y1 = hand.fingers[1].bone(0).next_joint[1]
					z1 = hand.fingers[1].bone(0).next_joint[2]
					
					x2 = hand.fingers[1].tip_position[0]
					y2 = hand.fingers[1].tip_position[1]
					z2 = hand.fingers[1].tip_position[2]	
					
					r = ( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )**0.5
				
					dist_norm = r/100

					if dist_norm >= 1:
						dist_norm=1

					CLAW_SERVO = abs(90-dist_norm*70)
					

					print 'Claw Angle =',CLAW_SERVO'''

					'''#EX1: DISTION TIP VS TIP
					x1 = hand.fingers[0].tip_position[0]
					y1 = hand.fingers[0].tip_position[1]
					z1 = hand.fingers[0].tip_position[2]

					x2 = hand.fingers[1].tip_position[0]
					y2 = hand.fingers[1].tip_position[1]
					z2 = hand.fingers[1].tip_position[2]
			
					r = ( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )**0.5

					dist_norm = r/100.

					if dist_norm >= 1:
						dist_norm=1
					
					CLAW_SERVO = abs(90-dist_norm*70)
					
					print 'Claw Angle =',CLAW_SERVO'''

					#CÁCH HAI: ANGLE_TO BONE VS BONE
					'''Vector1_index = hand.fingers[1].bone(0).direction
					Vector2_index = hand.fingers[1].bone(1).direction
					Bda_index = Vector1_index.angle_to(Vector2_index) * Leap.RAD_TO_DEG
					
					print Bda_index
					nor_angle = Bda_index/55
					if nor_angle >= 1:
						nor_angle = 1
					finger_servo = abs(90-nor_angle*70)
					
					print finger_servo'''


					#CÁCH BA: DOT BONE VS BONE
					Vector1_index = hand.fingers[4].bone(0).direction
					Vector2_index = hand.fingers[4].bone(1).direction
					Bda_index = Vector1_index.dot(Vector2_index) * Leap.RAD_TO_DEG

					print Bda_index

					nor_angle = (Bda_index-27)/30
					if nor_angle >= 1:
						nor_angle = 1
					if nor_angle <= 0:
						nor_angle = 0
					finger_servo = math.floor(abs(130+nor_angle*50))
					
					print finger_servo




			self.oldtime = self.newtime
		else:
			pass

def main():
	listener = LeapMotionListener()
	controller = Leap.Controller()

	controller.add_listener(listener)
	print ("Press enter to quit")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)

if __name__ == '__main__':
			main()      