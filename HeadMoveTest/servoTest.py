from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=8)
kit.servo[0].actuation_range = 120 #max FOR
while True:
	kit.servo[0].angle = 0
	for i in range(120):
		kit.servo[0].angle = i
		
		time.sleep(.1)
		print("Angle:" + str(kit.servo[0].angle))	


