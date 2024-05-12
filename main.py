import cv2

cap = cv2.VideoCapture(0) # Starts video capture with my camera (0).
# cap.set(3, 640) # Width (in px)
# cap.set(4, 480) # Length (in px)

imgBackground = cv2.imread("video-attendance-system/resources/background.png") # Background image GUI

while True: 
    success, img = cap.read()
    cv2.imshow("webcam", img) # Integrated webcam into background GUI
    cv2.imshow("face attendance", imgBackground) # Background for the GUI
    cv2.waitKey(1) # Wait-time in ms