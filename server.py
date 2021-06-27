# imports
import socket 
import threading

# define fixed length header (64 bytes)
HEADER = 64
# define an unused port
PORT = 4000
# define server (local ip address)
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
# define address
ADDR = (SERVER, PORT)
# define format
FORMAT = 'utf-8'
# define disconnect message
DISCONNECT_MESSAGE = "!disconnect"

# make a new socket (AF_INET family)
# bind socket to that address
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#store clients and their usernames in lists
clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

# to handle client, runs for EACH client
def handle_client(conn, addr):
    # print new connection
    print(f"NEW CONNECTION {addr} is connected.")
    
    # set connected to True
    connected = True
    while connected:
        # when receive information from client - blocking line
        # determine the message length
        rawMessage = conn.recv(HEADER)
        msg_length = rawMessage.decode(FORMAT)
        # if msg_length not null
        if msg_length:
            msg_length = int(msg_length)
            # receive the message
            msg = conn.recv(msg_length).decode(FORMAT)
            # if receive disconnect message, set connected to False
            if msg == DISCONNECT_MESSAGE:
                index = clients.index(conn)
                clients.remove(conn)
                conn.close()
                username = username[index]
                broadcast(f'{username} left the chat!'.encode(FORMAT))
                usernames.remove(username)
                connected = False
            else:
                broadcast(msg.encode(FORMAT))

            print(f"[{addr}] {msg}")
    # close the connection
    conn.close()
        
# to start socket server
def start():
    # listen to new connections
    server.listen()
    # print ip address server is listening to
    print(f"Server is LISTENING on {SERVER}")
    while True:
        # when new connection occur, store socket object(conn) and address(addr) - blocking line
        conn, addr = server.accept()
        #request and store username
        conn.send('USER'.encode(FORMAT))
        username = conn.recv(HEADER).decode(FORMAT)
        usernames.append(username)
        clients.append(conn)
        #print and broadcast username
        print("Nickname is {}".format(username))
        broadcast("{} joined!".format(username).encode(FORMAT))
        conn.send('Connected to server!'.encode(FORMAT))
        # start a new thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print how many threads are active in this process
        # -1 because start() thread is always running
        print(f"ACTIVE CONNECTIONS: {threading.activeCount() - 1}")


print("server is STARTING...")
start()

#python client.py