import cv2
import face_recognition
import pickle
import os

imgFaceDirectoryPath = "video-attendance-system/images"
imgFaceList = [] # Iterated through images directory to get all face images
imgFaceIdList = [] # Iterated through images directory names to get all face IDs
imgFacePathNameArray = os.listdir(imgFaceDirectoryPath) # Gets all the file names and puts in array for faces
for imgPath in imgFacePathNameArray:
    imgFaceList.append(cv2.imread(os.path.join(imgFaceDirectoryPath, imgPath)))
    imgFaceIdList.append(os.path.splitext(imgPath)[0])

def createEncodings(imgList): # Returns an face encoding for each image in an image list
    encodingList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encodingList.append(encoding)
    
    return encodingList

# Encodes all faces in images directory
print("Encoding process initiated...")
knownEncodingList = createEncodings(imgFaceList)
knownEncodingListWithIds = [knownEncodingList, imgFaceIdList]
print("Encoding process complete.")

# Dumps a file for all encodings on disk
encodingFile = open("video-attendance-system/EncodingFile.p", 'wb')
pickle.dump(knownEncodingListWithIds, encodingFile)
encodingFile.close()
print("File saved to disk.")