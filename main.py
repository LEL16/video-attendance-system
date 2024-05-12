import cv2
import os

cap = cv2.VideoCapture(0) # Starts video capture with my camera (0).
# cap.set(3, 640) # Width (in px)
# cap.set(4, 480) # Length (in px)

imgBackground = cv2.imread("video-attendance-system/resources/background.png") # Background image GUI

imgModeDirectoryPath = "video-attendance-system/resources/modes"
imgModeList = [] # Iterated through modes directory to get all mode images
imgModePathNameArray = os.listdir(imgModeDirectoryPath) # Gets all the file names and puts in array for modes
for imgPath in imgModePathNameArray:
    imgModeList.append(cv2.imread(os.path.join(imgModeDirectoryPath, imgPath)))

print(len(imgModeList))
while True: 
    success, img = cap.read()

    imgBackground[162:162 + 480, 55:55 + 640] = img # Overlays the webcam in the GUI

    cv2.imshow("webcam", img) # Integrated webcam into background GUI
    cv2.imshow("face attendance", imgBackground) # Background for the GUI
    cv2.waitKey(1) # Wait-time in ms