from socket import *
import cv2 as cv

address = '127.0.0.1'
port = 8090
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind((address, port))
print('bind success')
print('listening...')
server_sock.listen(1)

connection_sock, addr = server_sock.accept()

print(str(addr), 'tried to connect. check connection.')

while True:
    #key = cv.waitKey(1)
    data = connection_sock.recv(1024)
    #if key == 27:
    #    break
    print('received data: ', data)

connection_sock.send('server close the socket.')
print('close connection')
