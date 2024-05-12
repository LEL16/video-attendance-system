import cv2
import os
import face_recognition
import pickle
import numpy as np
import cvzone

cap = cv2.VideoCapture(0) # Starts video capture with my camera (0)
cap.set(3, 640) # Width (in px)
cap.set(4, 480) # Length (in px)

imgBackground = cv2.imread("video-attendance-system/resources/background.png") # Background image GUI

imgModeDirectoryPath = "video-attendance-system/resources/modes"
imgModeList = [] # Iterated through modes directory to get all mode images
imgModePathNameArray = os.listdir(imgModeDirectoryPath) # Gets all the file names and puts in array for modes
for imgPath in imgModePathNameArray:
    imgModeList.append(cv2.imread(os.path.join(imgModeDirectoryPath, imgPath)))

# Load an encoding file
print("Encoding loading process initiated...")
encodingFile = open('video-attendance-system/EncodingFile.p', 'rb')
knownEncodingListWithIds = pickle.load(encodingFile)
encodingFile.close()
knownFaceEncodingList, knownFaceStudentIdList = knownEncodingListWithIds
print("Encoding process complete.")

while True: 
    success, img = cap.read()

    imgResized = cv2.resize(img, (0, 0), None, 0.25, 0.25) # Resizes image to 1/4 to save computing power
    imgResized = cv2.cvtColor(imgResized, cv2.COLOR_BGR2RGB) # Converts image colors from BGR to RGB

    newFaceLocationCurrentFrame = face_recognition.face_locations(imgResized) # Gets the location of the face from the current frame
    newFaceEncodingCurrentFrame = face_recognition.face_encodings(imgResized, newFaceLocationCurrentFrame) # Gets the encoding of the face in the location specified in the current frame

    imgBackground[162 : 162 + 480, 55 : 55 + 640] = img # Overlays the webcam in the GUI
    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[2]

    for newFaceLocation, newFaceEncoding in zip(newFaceLocationCurrentFrame, newFaceEncodingCurrentFrame):
        faceMatches = face_recognition.compare_faces(knownFaceEncodingList, newFaceEncoding) # Compares known face encodings to current frame encodings to return boolean
        faceDistance = face_recognition.face_distance(knownFaceEncodingList, newFaceEncoding) # Calculate the distance from known encodings to current frame face encoding to return double
        faceMatchIndex = np.argmin(faceDistance) # Returns the index of the known face with the lowest distance
        if faceMatches[faceMatchIndex]:
            y1, x2, y2, x1 = newFaceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 # Rescales bounding box to original scale (not resized scale)
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1 # Creates bounding box with face locations
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0)
            

    cv2.imshow("face attendance", imgBackground) # Background for the GUI
    cv2.waitKey(1) # Wait-time in ms