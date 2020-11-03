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
        else: 
            cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 0, 0), 3) # black

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

center = ""
center_x, center_y = -1, -1
coordinate = []

list_ball_location = []
history_ball_locations = []
list_ball_location_R = []
history_ball_locations_R = []
list_ball_location_G = []
history_ball_locations_G = []
list_ball_location_B = []
history_ball_locations_B = []

isDraw = True
isFirst = False
draw_color = 'O'

# create coordinate log file
File = open("./log.txt", mode='w', encoding='utf-8')

while True:
    while True:
        # take a screenshot base picture
        #pic = pyautogui.screenshot(region=(0, 30, 1910 , 960))
        pic = pyautogui.screenshot(region=(0, 30, 960, 1015))
        img_frame = np.array(pic)
        img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
        
        data = conn_sock.recv(1024)
        if not data: break
        # data decoding: byte to str
        data = data.decode('utf-8')
        
        # process client string sign
        if 'quit' in data: break
        if 'stop' in data:
            if isFirst == False:
                isDraw = False
            else:
                continue
            data = data.replace('stop','')
        else:
            isDraw = True
            isFirst = False

        coor = data.split(']')
        for val in coor:
            if len(val) <= 1:
                continue
            center = val.split(',')
            center_x = int(center[0])
            center_y = int(center[1])
            list_ball_location.append((center_x, center_y))
        
        # write on log file
        fdata = "%d" % center_x
        fdata = fdata + ', ' + "%d" % center_y
        File.write(fdata + '\n')
        
        
        if isDraw:
            if draw_color == 'R':
                list_ball_location_R.append((center_x, center_y))
            elif draw_color == 'G':
                list_ball_location_G.append((center_x, center_y))
            elif draw_color == 'B':
                list_ball_location_B.append((center_x, center_y))
            else:
                list_ball_location.append((center_x, center_y))
        else:
            history_ball_locations_R.append(list_ball_location_R.copy())
            list_ball_location_R.clear()
            history_ball_locations_G.append(list_ball_location_G.copy())
            list_ball_location_G.clear()
            history_ball_locations_B.append(list_ball_location_B.copy())
            list_ball_location_B.clear()
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()

        if draw_color == 'R':
            draw_ball_location(img_frame, list_ball_location_R, draw_color)
        elif draw_color == 'G':
            draw_ball_location(img_frame, list_ball_location_G, draw_color)
        elif draw_color == 'B':
            draw_ball_location(img_frame, list_ball_location_B, draw_color)
        else:
            draw_ball_location(img_frame, list_ball_location, draw_color)
        
	    for ball_locations in history_ball_locations_R:
            draw_ball_location(img_frame, ball_locations, draw_color)
        for ball_locations in history_ball_locations_G:
            draw_ball_location(img_frame, ball_locations, draw_color)
        for ball_locations in history_ball_locations_B:
            draw_ball_location(img_frame, ball_locations, draw_color)
	    for ball_locations in history_ball_locations:
            draw_ball_location(img_frame, ball_locations, draw_color)
        
        #draw_ball_location(img_frame, list_ball_location, draw_color)

        cv.namedWindow("Window")
        cv.moveWindow("Window", 961, 30)
        cv.imshow('Window', img_frame)

        key = cv.waitKey(1)
        if key == 27:
            break
        elif key == ord('r'):
            draw_color = 'R'
        elif key == ord('g'):
            draw_color = 'G'
        elif key == ord('b'):
            draw_color = 'B'
        elif key == 32: # space bar
            list_ball_location_R.clear()
            list_ball_location_G.clear()
            list_ball_location_B.clear()
        elif key == ord('o'):
            draw_color = 'O'

    File.close()
    print("log file closed.")
    print("send closing msg to client.")
    conn_sock.send('server close the socket.'.encode())
    conn_sock.close()
    server_sock.close()
    print('close ALL connection')
    break
exit()
