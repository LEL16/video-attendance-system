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

ref = db.reference("Students") # Creates a directory named Students where data will be added

# All data per person written here
data = {
    "1" : 
        {
            "name" : "Lisul Elvitigala",
            "major" : "CS",
            "starting_year" : 2024,
            "total_attendance" : 6,
            "standing" : "G",
            "year" : 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2" : 
        {
            "name" : "Rajith Elvitigala",
            "major" : "Software Engineer",
            "starting_year" : 2000,
            "total_attendance" : 2,
            "standing" : "B",
            "year" : 4,
            "last_attendance_time": "2022-12-11 00:24:34"
        },
    "3" : 
        {
            "name" : "Uthpala Elvitigala",
            "major" : "Projects Engineer",
            "starting_year" : 2014,
            "total_attendance" : 1,
            "standing" : "A",
            "year" : 2,
            "last_attendance_time": "2022-12-11 00:54:24"
        },
    
}

imgFaceDirectoryPath = "video-attendance-system/images"
imgFaceList = [] # Iterated through images directory to get all face images
imgFacePathNameArray = os.listdir(imgFaceDirectoryPath) # Gets all the file names and puts in array for faces
for imgPath in imgFacePathNameArray:
    imgFaceList.append(cv2.imread(os.path.join(imgFaceDirectoryPath, imgPath)))

    storageFileName = f"{imgFaceDirectoryPath}/{imgPath}"
    storageBucket = storage.bucket() # Instantiates storage bucket
    storageBlob = storageBucket.blob(storageFileName)
    storageBlob.upload_from_filename(storageFileName) # Uploads face images to storage

for key, value in data.items():
    ref.child(key).set(value) # Sending values to a specific directory