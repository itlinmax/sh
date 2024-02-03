from datetime import datetime
import socket

server_address = ('10.1.1.2', 6789)
max_size = 100000

print('Starting the server at', datetime.now())
print('Waiting for a client to call.')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_address)
server.listen(5)
client, addr = server.accept()

data = client.recv(max_size)

print(data)
server.close()
