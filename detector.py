import cv2
import numpy as np
import face_recognition

imgelon_bgr = face_recognition.load_image_file('/training/elon_musk/161877.jpg')
imgelon_rgb = cv2.cvtColor(imgelon_bgr,cv2.COLOR_BGR2RGB)
cv2.imshow('bgr', imgelon_bgr)
cv2.imshow('rgb', imgelon_rgb)
cv2.waitKey(0)
# reset