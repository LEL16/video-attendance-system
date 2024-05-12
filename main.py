import cv2
import os
import face_recognition
import pickle
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
import cv2

# Connects to FireBase RealTime Database using key
cred = credentials.Certificate("C:/Users/uthpa/Videos/video-attendance-system/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL" : "https://lel16facerecognition-default-rtdb.firebaseio.com/",
    "storageBucket" : "lel16facerecognition.appspot.com"
})
storageBucket = storage.bucket()

cap = cv2.VideoCapture(0) # Starts video capture with my camera (0)
cap.set(3, 640) # Width (in px)
cap.set(4, 480) # Length (in px)

# Load background and modes
imgBackground = cv2.imread("video-attendance-system/resources/background.png") # Background image GUI

imgModeDirectoryPath = "video-attendance-system/resources/modes"
imgModeList = [] # Iterated through modes directory to get all mode images
imgModePathNameArray = os.listdir(imgModeDirectoryPath) # Gets all the file names and puts in array for modes
for imgPath in imgModePathNameArray:
    imgModeList.append(cv2.imread(os.path.join(imgModeDirectoryPath, imgPath)))
imgModeType = 0
imgModeCounter = 0
imgModeId = -1
imgModeStudent = []

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
    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[imgModeType] # Changes GUI to specific mode

    for newFaceLocation, newFaceEncoding in zip(newFaceLocationCurrentFrame, newFaceEncodingCurrentFrame):
        faceMatches = face_recognition.compare_faces(knownFaceEncodingList, newFaceEncoding) # Compares known face encodings to current frame encodings to return boolean
        faceDistance = face_recognition.face_distance(knownFaceEncodingList, newFaceEncoding) # Calculate the distance from known encodings to current frame face encoding to return double
        faceMatchIndex = np.argmin(faceDistance) # Returns the index of the known face with the lowest distance
        if faceMatches[faceMatchIndex]:
            y1, x2, y2, x1 = newFaceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 # Rescales bounding box to original scale (not resized scale)
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1 # Creates bounding box with face locations
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0) 
            imgModeId = knownFaceStudentIdList[faceMatchIndex] # Fetches student ID of matched face

            if imgModeCounter == 0:
                imgModeCounter = 1 # If there is a match, initiate counter
                imgModeType = 1 # If there is a match, change mode to display data
    
    if imgModeCounter != 0:
        if imgModeCounter == 1:
            # Fetching data
            detectedFaceStudentInfo = db.reference(f"Students/{imgModeId}").get() # Fetches all data from the matched student
            print(detectedFaceStudentInfo) 
            
            # Fetching image from storage
            storageBlob = storageBucket.get_blob(f"video-attendance-system/images/{imgModeId}.png")
            print(storageBlob)
            storageArray = np.frombuffer(storageBlob.download_as_string(), np.uint8)
            imgModeStudent = cv2.imdecode(storageArray, cv2.COLOR_BGR2RGB)

            # Update data for attendance
            ref = db.reference(f"Students/{imgModeId}")
            detectedFaceStudentInfo['total_attendance'] += 1 
            ref.child("total_attendance").set(detectedFaceStudentInfo["total_attendance"]) # Updates real-time database to local, larger attendance value
            
        if (10 < imgModeCounter < 20):
            imgModeType = 2

        imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[imgModeType]

        if (imgModeCounter <= 10):
            cv2.putText(imgBackground, str(detectedFaceStudentInfo["total_attendance"]), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1) # Displays total attendance in white
            cv2.putText(imgBackground, str(detectedFaceStudentInfo["major"]), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1) # Displays major in white
            cv2.putText(imgBackground, str(imgModeId), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1) # Displays major in white
            cv2.putText(imgBackground, str(detectedFaceStudentInfo["standing"]), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1) # Displays standing in white
            cv2.putText(imgBackground, str(detectedFaceStudentInfo["year"]), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1) # Displays year in white
            cv2.putText(imgBackground, str(detectedFaceStudentInfo["starting_year"]), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1) # Displays starting year in white

            (w, h), _ = cv2.getTextSize(detectedFaceStudentInfo["name"], cv2.FONT_HERSHEY_COMPLEX, 1, 1) # Gets width and height of the text
            nameOffset = 414 // 2 - w // 2 # Calculates offset needed for centering
            cv2.putText(imgBackground, str(detectedFaceStudentInfo["name"]), (808 + nameOffset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1) # Displays name in white

            imgBackground[175 : 175 + 216, 909 : 909 + 216] = imgModeStudent # Adds student image to GUI

        imgModeCounter += 1
    cv2.imshow("face attendance", imgBackground) # Background for the GUI
    cv2.waitKey(1) # Wait-time in ms