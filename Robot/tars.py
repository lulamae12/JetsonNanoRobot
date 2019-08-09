import numpy as np
import sys
import cv2
from adafruit_servokit import ServoKit



class Head(): #so no head?
    def __init__(self):

        self.kit = ServoKit(channels = 8)
        self.kit.servo[0].actuation_range = 120
        self.kit.servo[0].angle = 60 #starting default angle
        self.currentAngle = 60
        
    def moveHead(self,leftOrRight):	
	if leftOrRight == "left" and self.currentAngle + 1 <= 120:
		self.currentAngle = self.currentAngle + 1		
		self.kit.servo[0].angle = self.currentAngle
	elif leftOrRight == "right" and self.currentAngle - 1 >= 0:
		self.currentAngle = self.currentAngle - 1		
		self.kit.servo[0].angle = self.currentAngle
    def returnDirection(self,x):
        if(x <= 100):
            print("left")
            self.moveHead("left")
        # 550 350
        elif(x >= 250):
            print("right")
            self.moveHead("right")
    def saveKnownFaces(self):
        with open("knownFaces.dat", "wb") as face_data_file:
            face_data = [knownFaceEncodings, knownFaceMetadata]
            pickle.dump(face_data, face_data_file)
            print("Known faces saved to disk.")

    def loadKnownFaces(self):
        global known_face_encodings, known_face_metadata

        try:
            with open("knownFaces.dat", "rb") as faceDataFile:
                knownFaceEncodings, knownFaceMetadata = pickle.load(faceDataFile)
                print("Known faces loaded from disk.")
        except FileNotFoundError as e:
            print("No previous face data found - creating new list.")
            pass
    def addNewFace(self,faceEncoding,faceImage):
        knownFaceEncodings.append(faceEncoding)#add a new face encodings

        print("Hmm... I dont think i've seen you before, what is your name?")
        faceName = str(input("Name: "))

        knownFaceMetadata.append({
            "name":faceName,#add face name
        })

    def isFaceNew(self,faceEncoding):  #check if face has been seen before
        metadata = None

        if len(knownFaceEncodings) == 0:#face list is empty so its new
            return metadata

        faceSimilarity = face_recognition.face_distance(knownFaceEncodings,faceEncoding)#check perecnt sim between data in list
        print("similarity: " + str((faceSimilarity * 100 )) + "% ")

        bestMatchIndex = np.argmin(faceSimilarity)# get the most simialr face from face similarity

        if faceSimilarity[bestMatchIndex] < 0.65:

            metadata = knownFaceMetadata[bestMatchIndex]
        return metadata

    def mainLoop(self):
        loadKnownFaces() 
        video_capture = cv2.VideoCapture(0)

        numberOfFacesSinceSave = 0 # keep track of faces seen sicnce last save
    
        while True:


        #get a single frame
            ret, frame = video_capture.read()

        #resize frame for faster recog

            smallerFrame = cv2.resize(frame, (0,0), fx=0.50, fy=0.50)

            rgbSmallFrame = smallerFrame[:, :, ::-1]

        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = bodyCascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
















        #find faces

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                print("(",x,",",y,")")
                if(x < 200 and y < 200):
                    print("top left")
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "Face", (x, y), font, 1.0, (255, 255, 255), 1)


        #find all locations and face_encodings
            faceLocations = face_recognition.face_locations(rgbSmallFrame)
            faceEncodings = face_recognition.face_encodings(rgbSmallFrame, faceLocations)

            faceLabels = []

        # Loop through each detected face and see if it has been seen before
        # If so give it a label
            for faceLocation, faceEncoding in zip(faceLocations, faceEncodings):

                metadata = isFaceNew(faceEncoding)

                if metadata is not None:
                    faceNameLabel = metadata['name']
                    faceLabel = faceNameLabel
                else:
                    faceLabel = "Unknown!"

                # Grab the image of the the face from the current frame of video
                    top, right, bottom, left = faceLocation
                    faceImage = smallerFrame[top:bottom, left:right]
                    faceImage = cv2.resize(faceImage, (150, 150))

                #add new face
                    addNewFace(faceEncoding, faceImage)

                faceLabels.append(faceLabel)

        # Draw a box around each face and label each face
            for (top, right, bottom, left), faceLabel in zip(faceLocations, faceLabels):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

            # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, faceLabel, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                self.returnDirection(left)
        #show feed
            cv2.imshow("Video", frame)

        # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                saveKnownFaces()
                break

        # need to save our known faces back to disk every so often in case something crashes.
            if len(faceLocations) > 0 and numberOfFacesSinceSave > 100:
                saveKnownFaces()
                numberOfFacesSinceSave = 0
            else:
                numberOfFacesSinceSave += 1

    # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


head = Head()


while True:

    head.mainLoop()
    

