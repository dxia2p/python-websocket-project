import socket
import threading
from typing import Callable

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_TYPE_SPLITTER = '|'
MSG_END_IDENTIFIER = '&'

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

    @classmethod
    def handle_recv(cls):
        connected = True
        while connected:
            raw_msg = cls.client.recv(BUFFER_SIZE).decode(FORMAT)
            if raw_msg == DISCONNECT_MESSAGE:
                connected = False

            messages = raw_msg.split(MSG_END_IDENTIFIER) # This is in case multiple messages are combined into one by tcp
            for msg in messages:
                if msg == "": # There will always be a blank message at the end because of how split works, so it can be skipped
                    continue

                split_identifier_msg = msg.split(MSG_TYPE_SPLITTER, 1)
                if split_identifier_msg[0] in cls.recv_functions:
                    cls.recv_functions[split_identifier_msg[0]](split_identifier_msg[1])
                else:
                    print(f"Unknown message identifier [{split_identifier_msg[0]}]!")


    @staticmethod
    def send(identifier, msg):
        ClientNetworkHandler.client.send((identifier + MSG_TYPE_SPLITTER + msg + MSG_END_IDENTIFIER).encode(FORMAT))

    @classmethod
    def add_function(cls, messageIdentifier : str, function : Callable[[str], None]):
        cls.recv_functions[messageIdentifier] = function