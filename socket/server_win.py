from socket import *
import cv2 as cv
import numpy as np
import pyautogui
#import time
def draw_ball_location(img_color, locations):
    print("Enter the function")
    for i in range(len(locations) - 1):
        # if locations is empty
        if locations[0] is None or locations[1] is None:
            continue
        # draw each coordinates in locations on window
        # BGR of yellow = (0, 255, 255)
        print("draw something")
        cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 255, 255), 3)


def Bind_n_listen(addr, port_number):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((addr, port_number))
    print("binding success!")
    print("listening...")
    sock.listen(1)
    return sock

def Connect_to_client(sock):
    conn, addr = sock.accept()
    print(str(addr), "tried to connect.")
    return conn

def String_processing(sdata):
    # list values to str
    string = ''.join(sdata)
    
    print(string)
    print(type(string))

    if 'quit' in string:
        return -1, -1
    
    coor = string.split(']')
    '''
    if len(coor) <= 1:
    '''    
     
    string_coor = ''.join(coor)
    center = string_coor.split(',')
    center_x = int(center[0])
    center_y = int(center[1])
    print("center_x, center_y", center_x, center_y)
    print("\n")

    return center_x, center_y
        

address = '0.0.0.0'
port = 8090

server_sock = Bind_n_listen(address, port)
conn_sock = Connect_to_client(server_sock)

coordinate = []
list_ball_location = []
history_ball_locations = []
isDraw = True

File = open("./log.txt", mode='w', encoding='utf-8')

cv.namedWindow("Window")
cv.moveWindow("Window", 960, 0)

while True:
    '''
    # take a screenshot using base picture
    pic = pyautogui.screenshot(region=(0, 0, 1000, 960))
    #pic = pyautogui.screenshot()
    img_frame = np.array(pic)
    img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
    '''
    while True:
        
        # take a screenshot using base picture
        pic = pyautogui.screenshot(region=(0, 0, 1000, 960))
        #pic = pyautogui.screenshot()
        img_frame = np.array(pic)
        img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
        
        data = conn_sock.recv(1024)
        if not data: break
        # data decoding: byte to str
        data = data.decode('utf-8')
        if 'quit' in data: break
        coor = data.split(']')
        for val in coor:
            if len(val) <= 1:
                continue
            center = val.split(',')
            center_x = int(center[0])
            center_y = int(center[1])
            list_ball_location.append((center_x, center_y))
        '''
        center_x, center_y = String_processing(data)
        
        if center_x == -1 and  center_y == -1:
            break
        '''
        # write on log file
        fdata = "%d" % center_x
        fdata = fdata + ', ' + "%d" % center_y
        File.write(fdata + '\n')
        
        #list_ball_location.append((center_x, center_y))

        '''
        if isDraw:
            list_ball_location.append((center_x, center_y))
        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()
        
        draw_ball_location(img_frame, list_ball_location)
    
        for ball_locations in history_ball_locations:
            draw_ball_location(img_frame, ball_locations)
        '''
        draw_ball_location(img_frame, list_ball_location)
        cv.imshow('Window', img_frame)

        key = cv.waitKey(1)
        if key == 27:
            break

    File.close()
    print("log file closed.")
    print("send closing msg to client.")
    conn_sock.send('server close the socket.'.encode())
    conn_sock.close()
    server_sock.close()

    print('close ALL connection')
    break

