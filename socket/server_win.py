from socket import *
import cv2 as cv
import numpy as np
import pyautogui

def draw_ball_location(img_color, locations, color):
    for i in range(len(locations) - 1):
        # if locations is empty
        if locations[0] is None or locations[1] is None:
            continue
        # draw each coordinates in locations on window
        if color == 'R':
            cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 0, 255), 3)
        elif color == 'B':
            cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (255, 0, 0), 3)
        elif color == 'G':
            cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 255, 0), 3)
        elif color == 'O': 
            cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 0, 0), 3) # black
    return img_color

def Bind_n_listen(addr, port_number):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((addr, port_number))
    print("binding success!")
    sock.listen(1)
    print("listening...")
    return sock

def Connect_to_client(sock):
    conn, addr = sock.accept()
    print(str(addr), "tried to connect.")
    return conn

address = '0.0.0.0' # INADDR_ANY
port = 8090

server_sock = Bind_n_listen(address, port)
conn_sock = Connect_to_client(server_sock)

coordinate = []

list_ball_location = []
history_ball_locations = []
list_ball_location_R = []
history_ball_locations_R = []
list_ball_location_G = []
history_ball_locations_G = []
list_ball_location_B = []
history_ball_locations_B = []

draw_color = 'O'

# create coordinate log file
File = open("./log.txt", mode='w', encoding='utf-8')

while True:
    # take a screenshot base picture
    #pic = pyautogui.screenshot(region=(0, 30, 1910 , 960))
    pic = pyautogui.screenshot(region=(0, 30, 1919, 1015))
    img_frame = np.array(pic)
    img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
    
    data = conn_sock.recv(1024)
    # data decoding: byte to str
    data = data.decode('utf-8')
    
    # process client string sign
    if 'quit' in data: break
    if data is not None:
        coor = data.split(']')
        for val in coor:
            if len(val) <= 1:
                continue
            center = val.split(',')
            center_x = int(center[0])
            center_y = int(center[1])
        
            # write on log file
            fdata = "%d" % center_x
            fdata = fdata + ', ' + "%d" % center_y
            File.write(fdata + '\n')

            if draw_color == 'R':
                list_ball_location_R.append((center_x, center_y))
            elif draw_color == 'G':
                list_ball_location_G.append((center_x, center_y))
            elif draw_color == 'B':
                list_ball_location_B.append((center_x, center_y))
            elif draw_color == 'O':
                list_ball_location.append((center_x, center_y))
            
            history_ball_locations_R.append(list_ball_location_R.copy())
            history_ball_locations_G.append(list_ball_location_G.copy())
            history_ball_locations_B.append(list_ball_location_B.copy())
            history_ball_locations.append(list_ball_location.copy())
    '''        
    else:
        history_ball_locations_R.append(list_ball_location_R.copy())
        list_ball_location_R.clear()
        history_ball_locations_G.append(list_ball_location_G.copy())
        list_ball_location_G.clear()
        history_ball_locations_B.append(list_ball_location_B.copy())
        list_ball_location_B.clear()
        history_ball_locations.append(list_ball_location.copy())
        list_ball_location.clear()
    '''
    for ball_locations in history_ball_locations_R:
        img_frame = draw_ball_location(img_frame, ball_locations, 'R')
    for ball_locations in history_ball_locations_G:
        img_frame = draw_ball_location(img_frame, ball_locations, 'G')
    for ball_locations in history_ball_locations_B:
        img_frame = draw_ball_location(img_frame, ball_locations, 'B')
    for ball_locations in history_ball_locations:
        img_frame = draw_ball_location(img_frame, ball_locations, 'O') # black

    if draw_color == 'R':
        img_frame = draw_ball_location(img_frame, list_ball_location_R, draw_color)
    elif draw_color == 'G':
        img_frame = draw_ball_location(img_frame, list_ball_location_G, draw_color)
    elif draw_color == 'B':
        img_frame = draw_ball_location(img_frame, list_ball_location_B, draw_color)
    elif draw_color == 'O':
        img_frame = draw_ball_location(img_frame, list_ball_location, draw_color)

    cv.namedWindow("Window")
    cv.moveWindow("Window", 1921, 30)
    cv.imshow('Window', img_frame)
    key = cv.waitKey(1)

    if key == 27:
        break
    elif key == ord('r'):
        draw_color = 'R'
        print("press R key")
    elif key == ord('g'):
        draw_color = 'G'
        print("press G key")
    elif key == ord('b'):
        draw_color = 'B'
        print("press B key")
    elif key == ord('o'):
        draw_color = 'O'
        print("press O key")
    elif key == 32: # space bar
        list_ball_location_R.clear()
        history_ball_locations_R.clear()
        list_ball_location_G.clear()
        history_ball_locations_G.clear()
        list_ball_location_B.clear()
        history_ball_locations_B.clear()
        list_ball_location.clear()
        history_ball_locations.clear()

File.close()
print("log file closed.")
print("send closing msg to client.")
conn_sock.send('server close the socket.'.encode())
conn_sock.close()
server_sock.close()
print('close ALL connection')
