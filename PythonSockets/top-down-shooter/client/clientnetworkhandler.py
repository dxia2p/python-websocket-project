import socket
import threading
from typing import Callable

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class ClientNetworkHandler:
    port = -1
    ip = ""
    client = None

    recvFunctions = {}
    onJoinCallback = None

    @staticmethod
    def initialize(ip = socket.gethostbyname(socket.gethostname()), port = 6969, onJoinCallback = lambda : None):
        ClientNetworkHandler.ip = ip
        ClientNetworkHandler.port = port
        ClientNetworkHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ClientNetworkHandler.client.connect((ip, port))
        ClientNetworkHandler.onJoinCallback = onJoinCallback
        #ClientNetworkHandler.server.settimeout(2.0)

        print(f"[CONNECTED TO SERVER ON {ip}:{port}]")
        handle_recv_thread = threading.Thread(target=ClientNetworkHandler.handle_recv, daemon=True)

    @staticmethod
    def handle_recv():
        while True:
            msg = ClientNetworkHandler.client.recv(BUFFER_SIZE)
            print(msg)

    @staticmethod
    def send(msg):
        message = msg.encode(FORMAT)
        ClientNetworkHandler.client.send(message)


    """
    @staticmethod
    def AcceptClients():
        while True:
            conn, addr = ClientNetworkHandler.server.accept()
            thread = threading.Thread(target=ClientNetworkHandler.HandleClient, args=(conn, addr), daemon=True)
            thread.start()
            ClientNetworkHandler.onJoinCallback()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

    @staticmethod
    def HandleClient(conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected: # LOGIC FOR RECIEVING DATA GOES HERE

            msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            splitMsg = msg.split('|') # All messages should have this character after the identifier for the data in the message

            if splitMsg[0] in ClientNetworkHandler.recvFunctions:
                ClientNetworkHandler.recvFunctions[splitMsg[0]](splitMsg[1])

        conn.close()
    """
    
    def AddFunction(messageIdentifier : str, function : Callable[[str], None]):
        ClientNetworkHandler.recvFunctions[messageIdentifier] = function