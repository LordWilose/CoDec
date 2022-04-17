import socket

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004

print('Waiting for connection response...')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

data = ClientMultiSocket.recv(1024)
print(data.decode('utf-8'))
dst = input("Destination (0, 1, 2...) : ")
ClientMultiSocket.send(dst.encode('utf-8'))

while True:
    Input = input('Type here: ')

    if Input == "":
        break
    else:
        ClientMultiSocket.send(str.encode(Input))
        data = ClientMultiSocket.recv(1024)
        print(data.decode('utf-8'))

ClientMultiSocket.close()