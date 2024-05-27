import socket
import threading
from typing import Callable

HEADER = 32
BUFFER_SIZE = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_TYPE_SPLITTER = '|'

class ClientNetworkHandler:
    port = -1
    ip = ""
    client = None

    recv_functions = {}
    on_join_callback = None

    @classmethod
    def initialize(cls, ip = socket.gethostbyname(socket.gethostname()), port = 6969, on_join_callback = lambda : None):
        cls.ip = ip
        cls.port = port
        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.client.connect((ip, port))
        cls.on_join_callback = on_join_callback
        #ClientNetworkHandler.server.settimeout(2.0)

        cls.on_join_callback()
        print(f"[CONNECTED TO SERVER ON {ip}:{port}]")
        handle_recv_thread = threading.Thread(target=cls.handle_recv, daemon=True)
        handle_recv_thread.start()

    @classmethod
    def handle_recv(cls):
        connected = True
        while connected:
            try:
                msg_length = cls.client.recv(HEADER, socket.MSG_WAITALL).decode(FORMAT)
                if msg_length: # Check if the message is none
                    msg_length = int(msg_length)
                    msg = cls.client.recv(msg_length, socket.MSG_WAITALL).decode(FORMAT)

                    split_msg = msg.split(MSG_TYPE_SPLITTER, 1) # All messages should have this character after the identifier for the data in the message
                    if split_msg[1] == DISCONNECT_MESSAGE:
                        connected = False
                        continue

                    if split_msg[0] in cls.recv_functions:
                        cls.recv_functions[split_msg[0]](split_msg[1])
                    else:
                        print(f"Unknown message identifier [{split_msg[0]}]")
            except Exception as ex:
                print(ex)

    @classmethod
    def send(cls, identifier, msg):
        """Starts a new thread and sends the message specified after sending the length of the message"""
        thread = threading.Thread(target=cls.send_thread, args=(identifier, msg))
        thread.start()

    @classmethod
    def send_thread(cls, identifier, msg):
        """Do not call this directly"""
        message = (identifier + MSG_TYPE_SPLITTER + msg).encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        cls.client.sendall(send_length)
        cls.client.sendall(message)

    @classmethod
    def add_function(cls, messageIdentifier : str, function : Callable[[str], None]):
        cls.recv_functions[messageIdentifier] = function