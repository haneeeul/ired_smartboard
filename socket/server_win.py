from socket import *

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(('127.0.0.1', 8081))
server_sock.listen(1)

connection_sock, addr = server_sock.accept()

print(str(addr), 'tried to connect. check connection.')

data = connection_sock.recv(1024)
print('received data: ', data)

connection_sock.send('I am a server.')
print('send message')
