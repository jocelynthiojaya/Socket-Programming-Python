# imports
import socket
import threading

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

username = input("Input your username: ")

# make a new socket (AF_INET family)
# bind socket to that address
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive():
    connected = True
    while connected:
        try:
            # Receive Message From Server
            # If 'USER' Send Username
            message = client.recv(HEADER).decode(FORMAT)
            if message == 'USER':
                client.send(username.encode(FORMAT))
            else:
                print(message)
        except:
            print("aight ima head out")
            client.close()
            connected = False


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


def write():
    connected = True
    while connected:
        # send the message in username: message format
        message = '{}: {}'.format(username, input(''))
        send(message)
        if DISCONNECT_MESSAGE in message:
            connected = False
            client.close()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
