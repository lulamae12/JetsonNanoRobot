# pip install opencv-python
import numpy as np
import sys
import cv2
from adafruit_servokit import ServoKit
kit = ServoKit(channels=8)
kit.servo[0].actuation_range = 120 #max FOR
kit.servo[0].angle = 60 #def angle
currentAngle = 60


Left = False
Right = False

bodyCascPath = 'haarcascade_frontalface_alt.xml'
faceCascPath = 'haarcascade_frontalface.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)
bodyCascade = cv2.CascadeClassifier(bodyCascPath)
def moveHead(leftOrRight):
	global currentAngle	
	if leftOrRight == "left" and currentAngle + 1 <= 120:
		currentAngle = currentAngle + 1		
		kit.servo[0].angle = currentAngle
	elif leftOrRight == "right" and currentAngle - 1 >= 0:
		currentAngle = currentAngle - 1		
		kit.servo[0].angle = currentAngle

def returnDirection(x):
    if(x <= 100):
        print("left")
        moveHead("left")
    # 550 350
    elif(x >= 250):
        print("right")
        moveHead("right")
defaultcam = cv2.VideoCapture(0)
#
while(True):
    ret, frame = defaultcam.read()  # returns t/f if frame is read corr
    frame = cv2.resize(frame, (0, 0), fx=.5, fy=.5)
    frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(10, 10),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    bodies = bodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(10, 10),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print("(", x, ",", y, ")")
        returnDirection(x)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Face", (x, y), font, 1.0, (255, 255, 255), 1)
# Draw a rectangle around the body
    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print("(", x, ",", y, ")")
        returnDirection(x)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "person", (x, y), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Press "q" to exit', frame)
    print(Right)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
defaultcam.release()
cv2.destroyAllWindows()
