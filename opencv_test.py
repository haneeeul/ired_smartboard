import cv2

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(-1)

cap.set(3, 720)
cap.set(4, 1080)

while True:
    ret, frame = cap.read()
    cv2.imshow('test',frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release(-1)
cv2.destroyAllWindows()
