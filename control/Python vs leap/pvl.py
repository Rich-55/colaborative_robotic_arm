# -*- coding: utf-8 -*-
#Tạo chương chình lấy thông tin từ leap motion
#import thư viện
import Leap, sys, thread, time
#import các loại cử chỉ
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
		if self.newtime - self.oldtime > 0:
			
			frame = controller.frame()
		
			'''print " Frame ID: " + str(frame.id)\
			+ " Timestamp: " + str(frame.timestamp)\
			+ " # of Hands: " + str(len(frame.hands))\
			+ " # of Fingers: " + str(len(frame.fingers))\
			+ " # of Tools: " + str(len(frame.tools))\
			+ " # of Gestures: " + str(len(frame.gestures()))'''
		 
			for hand in frame.hands:
				handType = " Left Hand " if hand.is_left else " Right Hand "
		
				#print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)

				normal = hand.palm_normal
				direction = hand.direction
				print " Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: " + str( direction.yaw * Leap.RAD_TO_DEG)
				'''old.dir = direction.pitch
				new.dir = direction.pitch
				P = new.dir - old.dir
				print P'''

				'''arm = hand.arm
				print " Arm Direction: " + str(arm.direction),
				" Wrist Position: " + str(arm.wrist_position),
				" Elbow Position: " + str(arm.elbow_position)'''
			
				for finger in hand.fingers:
				
					#print " Type: " + self.finger_names[finger.type], " ID: " + str(finger.id), " Length(mm): " + str(finger.length), " Width(mm): " + str(finger.width)

					'''for b in range(0, 4):
						bone = finger.bone(b)
						print " Bone: " + self.bone_names[bone.type]
						print " Start: " + str(bone.prev_joint)
						print " End: " + str(bone.next_joint)
						print " Direction: " + str(bone.direction)'''


					'''x1 = hand.fingers[1].bone(0).next_joint[0]
					y1 = hand.fingers[1].bone(0).next_joint[1]
					z1 = hand.fingers[1].bone(0).next_joint[2]
					
					x2 = hand.fingers[1].tip_position[0]
					y2 = hand.fingers[1].tip_position[1]
					z2 = hand.fingers[1].tip_position[2]

					d = ( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )**0.5

					print d'''


					
					'''Vector1_index = hand.fingers[1].bone(0).direction
					Vector2_index = hand.fingers[1].bone(1).direction
					Bda_index = Vector1_index.dot(Vector2_index) * Leap.RAD_TO_DEG


					print Bda_index'''



			'''for tool in frame.tools:
				print "Tool ID: " + str(tool.id),
				" Tip Position: " + str(tool.tip_position),
				" Direction: " + str (tool.direction)'''


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