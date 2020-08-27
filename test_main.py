# from https://webnautes.tistory.com
import cv2 as cv # opencv __version__ 4.2.0
from socket import *

# parameter 0 means main web camera
cap = cv.VideoCapture(0)

list_ball_location = []
history_ball_locations = []
isDraw = False # Do not draw as soon as the program starts

# make socket
client_sock = socket(AF_INET, SOCK_STREAM)
client_sock.connect(('192.168.35.176', 8090))

print('connection success')
client_sock.send(str('client: connection is okay').encode())

# __main()__
while cap.isOpened():
    # loading video
    ret,img_color = cap.read()

    # make video colorful. Using parameter cv2.COLOT_BGR@HSV
    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    ## for color detection
    hue_red = 170 # HSV red value
    lower_red = (hue_red-10, 0, 240)
    upper_red = (hue_red+10, 255, 255)

    ## detect between lower_red and upper_red color
    img_mask = cv.inRange(img_hsv, lower_red, upper_red)

    # make circle structuring element for segmentation
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    # combination of erosion and dilation
    # use cv2.morphologyEx(). erosion and dilation for iterations=3 times
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations = 3)
    # labeling
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1

    for i in range(nlabels):

        if i < 1:
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max:
            max = area
            max_index = i

    if max_index != -1:
        # make a circle and square
        center_x = int(centroids[max_index, 0]) 
        center_y = int(centroids[max_index, 1])
        left = stats[max_index, cv.CC_STAT_LEFT]
        top = stats[max_index, cv.CC_STAT_TOP]
        width = stats[max_index, cv.CC_STAT_WIDTH]
        height = stats[max_index, cv.CC_STAT_HEIGHT]

        cv.rectangle(img_color, (left, top), (left + width, top + height), (0, 0, 255), 5)
        cv.circle(img_color, (center_x, center_y), 10, (0, 255, 0), -1)

        client_sock.send((str(center_x)+','+str(center_y)).encode())

        # create window and show the result
        cv.imshow('Binarization', img_mask)
        cv.imshow('Result', img_color)

        # Using keyboard function for drawing or not or clear all
        key = cv.waitKey(1)
        if key == 27: # esc
            break

print('main() is ended')
data = client_sock.recv(1024)
print('received data:', data.decode())
client_sock.close()