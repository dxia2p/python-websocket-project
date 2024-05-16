import threading
import socket
import serverPlayer

HEADER = 64
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

players = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected: # LOGIC GOES HERE
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: # check if message is none
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if(msg == DISCONNECT_MESSAGE):
                connected = False
            print(f"[{addr}] {msg}")
            
            if msg[0] == 'i':
                pass

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # each client is connected on a new thread
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()