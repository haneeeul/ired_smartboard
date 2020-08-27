import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        cv2.imshow('Camera Window', frame)

        key = cv2.waitKey(1) & 0xFF
        if (key == 27):
            break

cap.release()
cv2.destroyAllwindows()
