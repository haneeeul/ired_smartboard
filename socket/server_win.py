from socket import *
import cv2 as cv
import time

address = '127.0.0.1'
port = 8000
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((address, port))
print('bind success')
print('listening...')
server_sock.listen(1)

connection_sock, addr = server_sock.accept()

print(str(addr), 'tried to connect. check connection.')

while True:
    
    data = connection_sock.recv(1024)
    # data decoding
    # byte to str
    data = data.decode('utf-8')
    coordinate = data.split(']')
    for val in coordinate:
        if len(val) <= 1:
            continue
        center = val.split(',')
        center_x = int(center[0])
        center_y = int(center[1])
        print('the coordinate is: ', center_x, end=' ')
        print(', ', center_y)
        #time.sleep(1)

    print('check key value')
    key = cv.waitKey(0)
    if key == 27:
        break

connection_sock.send('server close the socket.'.encode())
connection_sock.close()
server_sock.close()

print('close ALL connection')
