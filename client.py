# imports
import socket

# define fixed length header (64 bytes)
HEADER = 64
# define an unused port
PORT = 4000
# define format
FORMAT = 'utf-8'
# define disconnect message
DISCONNECT_MESSAGE = "!disconnect"
# define server (local ip address)
SERVER = socket.gethostbyname(socket.gethostname())
# define address
ADDR = (SERVER, PORT)

# make a new socket (AF_INET family)
# bind socket to that address
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    # encode string into byte size object
    message = msg.encode(FORMAT)
    # get the length of message
    msg_length = len(message)
    # padding to become length of 64 bytes
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # send to client
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

connected = True
while connected:
    message = input()
    send(message)
    if message == DISCONNECT_MESSAGE:
        connected = False