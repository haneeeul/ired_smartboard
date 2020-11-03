import sys
import cv2 as cv # opencv __version__ 4.1.1
from socket import *

def Exit(argv, sock):
    if argv == 1:
        cv.destroyAllWindows()
        print('system: main() is ended')
        buf = sock.recv(1024)
        print('serv msg: ', buf.decode());
        print('system: Close client socket')
        sock.close()
        print('bye')
    
# parameter 0 means main pi camera
cap = cv.VideoCapture(0)

# socket
if len(sys.argv) < 3:
    print("ERROR!\nUsage: python3opencv main.py <IP address> <Port>")
    cv.destroyAllWindows()
    exit()
else:
    addr = sys.argv[1]
    port = int(sys.argv[2])

client_sock = socket(AF_INET, SOCK_STREAM)
client_sock.connect((addr, port))
print('connection success')

if not cap.isOpened():
    cap.open()

# __main()__
while True:
    # loading video
    ret,img_color = cap.read()

    # make video colorful. Using parameter cv2.COLOT_BGR@HSV
    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    ## for color detection
    hue_red = 150 # HSV
    lower_red = (hue_red - 10, 0, 200)
    upper_red = (hue_red + 10, 255, 255)

    ## detect between lower_red and upper_red color
    ## if color of pixel is not in range between lower_red and upper_red, is black 
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
        # make a circle
        center_x = int(centroids[max_index, 0]) 
        center_y = int(centroids[max_index, 1])
        
        cv.circle(img_color, (center_x, center_y), 10, (0, 255, 0), -1)

        # send coordinate x and y
        client_sock.send((str(center_x)+','+str(center_y)+']').encode())

    # create window and show the result
    cv.imshow('Binarization', img_mask)
    cv.imshow('Result', img_color)

    # Using keyboard function for break
    key = cv.waitKey(1)
    if key == 27: # esc
        client_sock.send('quit'.encode())
        break

Exit(1, client_sock)
