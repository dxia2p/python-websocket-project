import socket
import threading
from typing import Callable

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class ServerNetworkHandler:
    port = -1
    ip = ""
    server = None

    recv_functions = {}
    clientAddedCallback = None

    @classmethod
    def Initialize(cls, ip = socket.gethostbyname(socket.gethostname()), port = 6969, clientAddedCallback = lambda : None):
        cls.ip = ip
        cls.port = port
        cls.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.server.bind((ip, port))
        cls.clientAddedCallback = clientAddedCallback
        #cls.server.settimeout(2.0)

        cls.server.listen()
        print(f"[LISTENING] Server is listening on {ip} : {port}")
        accept_clients_thread = threading.Thread(target=cls.accept_clients)
        accept_clients_thread.start()

    @classmethod
    def accept_clients(cls):
        while True:
            conn, addr = cls.server.accept()
            thread = threading.Thread(target=cls.handle_client, args=(conn, addr), daemon=True)
            thread.start()
            cls.clientAddedCallback()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

    @classmethod
    def handle_client(cls, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected: # LOGIC FOR RECIEVING DATA GOES HERE

            msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            splitMsg = msg.split('|') # All messages should have this character after the identifier for the data in the message

            if splitMsg[0] in cls.recv_functions:
                cls.recv_functions[splitMsg[0]](splitMsg[1])

        conn.close()
    
    @classmethod
    def AddFunction(cls, messageIdentifier : str, function : Callable[[str], None]):
        cls.recv_functions[messageIdentifier] = function