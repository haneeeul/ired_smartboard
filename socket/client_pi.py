from socket import *

client_sock = socket(AF_INET, SOCK_STREAM)
client_sock.connect(('192.168.35.176', 8090))

print('connection success')
client_sock.send(str('I am client').encode())

print('message sending')

data = client_sock.recv(1024)
print('received data: ', data.decode())
