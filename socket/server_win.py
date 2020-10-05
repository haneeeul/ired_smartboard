from socket import *
import cv2 as cv
import numpy as np
import pyautogui
#import time

def draw_ball_location(img_color, locations):
    for i in range(len(locations) - 1):
        # if locations is empty
        if locations[0] is None or locations[1] is None:
            continue

        # draw each coordinates in locations on window
        # BGR of yellow = (0, 255, 255)
        cv.line(img_color, tuple(locations[0]), tuple(locations[1]), (0, 255, 0), 3)
'''
address = '0.0.0.0'
port = 8090
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((address, port))
print('bind success')
print('listening...')
server_sock.listen(1)

connection_sock, addr = server_sock.accept()

print(str(addr), 'tried to connect. check connection.')
'''

coordinate = []
list_ball_location = []
history_ball_locations = []
isDraw = True
#File = open("./log.txt", mode='w', encoding='utf-8')
File = open("./log.txt", mode='r')

cv.namedWindow("Window")
cv.moveWindow("Window", 960, 0)
while True:
    pic = pyautogui.screenshot(region=(0, 0, 1000, 960))
    #pic = pyautogui.screenshot()
    img_frame = np.array(pic)
    img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
    
    #data = connection_sock.recv(1024)
    data = File.readline()
    if not data: break
    '''
    # data decoding
    # byte to str
    data = data.decode('utf-8')
    
    # check quit sign
    if data == 'quit':
        break
    coordinate = data.split(']')
    '''
    coordinate = data
    for val in coordinate:
        if len(val) <= 1:
            continue
        
        center = val.split(", ")
        center_x = int(center[0])
        center_y = int(center[1])
        print("center_x, center_y", center_x, center_y)
        print("\n")
        '''
        fdata = "%d" % center_x
        fdata = fdata + ', ' + "%d" % center_y
        File.write(fdata + '\n')
        '''
        if isDraw:
            list_ball_location.append((center_x, center_y))
        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()

    draw_ball_location(img_frame, list_ball_location)

    for ball_locations in history_ball_locations:
        draw_ball_location(img_frame, ball_locations)
        
    cv.imshow('Window', img_frame)

    key = cv.waitKey(1)
    if key == 27:
        break

#File.close()
connection_sock.send('server close the socket.'.encode())
connection_sock.close()
server_sock.close()

print('close ALL connection')
