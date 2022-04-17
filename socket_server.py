import socket
import os
from _thread import *


def multi_threaded_client(connection, dsts):
    connection.sendall(str.encode("Destination :\n%s"%(dsts)))
    dst = connection.recv(2048).decode('utf-8')
    destination = dsts[int(dst)][1]
    while True:
        data = connection.recv(2048)
        if not data:
            break
        destination.sendall(data)
        connection.sendall("Done.".encode('utf-8'))
    connection.close()


ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening...')
ServerSideSocket.listen(5)
dsts = {}

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    dsts[ThreadCount] = [str(address[0])+":"+str(address[1]), Client]
    start_new_thread(multi_threaded_client, (Client, dsts))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()