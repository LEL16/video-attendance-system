import cv2
from ultralytics import YOLO
import numpy as np

cap = cv2.VideoCapture("video/test/lisul.mp4")
model = YOLO("yolov8m.pt")

while True:
    # Reads frame by frame
    ret, frame = cap.read()
    # If there's no frame to be read
    if not ret:
        break

    # Detects objects in frame
    results = model(frame, device="mps")
    # First result
    result = results[0]
    # Get bounding boxes
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype=int)
    # 
    classes = np.array(result.boxes.cls.cpu(), dtype=int)
    for cls, bbox in zip(classes, bboxes):
        (x, y, x2, y2) = bbox

        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, str(cls), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Img", frame)
    # Time frame is showed (in ms). 0 means infinite time / until key is pressed.
    key = cv2.waitKey(1)
    # Key 27 is escape key.
    if key == 27:
        break

# Stop python lock on video file. Destroy all cv2 windows.
cap.release()
cv2.destroyAllWindows()