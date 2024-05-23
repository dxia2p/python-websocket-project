import socket
import threading
from typing import Callable

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_SPLIT_IDENTIFIER = '|'

class ClientNetworkHandler:
    port = -1
    ip = ""
    client = None

    recv_functions = {}
    on_join_callback = None

    @staticmethod
    def initialize(ip = socket.gethostbyname(socket.gethostname()), port = 6969, on_join_callback = lambda : None):
        ClientNetworkHandler.ip = ip
        ClientNetworkHandler.port = port
        ClientNetworkHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ClientNetworkHandler.client.connect((ip, port))
        ClientNetworkHandler.on_join_callback = on_join_callback
        #ClientNetworkHandler.server.settimeout(2.0)

        ClientNetworkHandler.on_join_callback()
        print(f"[CONNECTED TO SERVER ON {ip}:{port}]")
        handle_recv_thread = threading.Thread(target=ClientNetworkHandler.handle_recv, daemon=True)
        handle_recv_thread.start()

    @staticmethod
    def handle_recv():
        connected = True
        while connected:
            msg = ClientNetworkHandler.client.recv(BUFFER_SIZE).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            split_msg = msg.split(MSG_SPLIT_IDENTIFIER, 1)
            if split_msg[0] in ClientNetworkHandler.recv_functions:
                ClientNetworkHandler.recv_functions[split_msg[0]](split_msg[1])
            


    @staticmethod
    def send(msg):
        message = msg.encode(FORMAT)
        ClientNetworkHandler.client.send(message)

    @classmethod
    def add_function(cls, messageIdentifier : str, function : Callable[[str], None]):
        cls.recv_functions[messageIdentifier] = function