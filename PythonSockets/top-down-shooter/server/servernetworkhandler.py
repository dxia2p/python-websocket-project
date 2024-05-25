import socket
import threading
from typing import Callable

HEADER = 32
BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_TYPE_SPLITTER = '|'

class ServerNetworkHandler:
    port = -1
    ip = ""
    server = None

    recv_functions = {}
    client_added_callback = None
    client_removed_callback = None

    clients = []

    @classmethod
    def initialize(cls, client_added_callback : Callable[[socket.socket], None], client_removed_callback : Callable[[socket.socket], None], ip = socket.gethostbyname(socket.gethostname()), port = 6969):
        cls.ip = ip
        cls.port = port
        cls.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.server.bind((ip, port))
        cls.client_added_callback = client_added_callback
        cls.client_removed_callback = client_removed_callback
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
            cls.clients.append(conn)
            cls.client_added_callback(conn)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

    @classmethod
    def handle_client(cls, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected: # LOGIC FOR RECIEVING DATA GOES HERE

            msg_length = conn.recv(HEADER, socket.MSG_WAITALL).decode(FORMAT)
            if msg_length: # check if the message is none
                msg_length = int(msg_length)
                msg = conn.recv(msg_length, socket.MSG_WAITALL).decode(FORMAT)

                split_msg = msg.split(MSG_TYPE_SPLITTER, 1) # All messages should have this character after the identifier for the data in the message
                if(split_msg[1] == DISCONNECT_MESSAGE):
                    connected = False
                    continue

                if split_msg[0] in cls.recv_functions:
                    cls.recv_functions[split_msg[0]](conn, split_msg[1])
                else:
                    print(f"Unknown message identifier [{split_msg[0]}]!")

        cls.client_removed_callback(conn)
        cls.clients.remove(conn)
        conn.close()

    @classmethod
    def send_to_all(cls, identifier, msg):
        """Starts a thread for each client and sends the provided message to all sockets connected to this server"""
        for conn in cls.clients:
            thread = threading.Thread(target=cls.send_to_conn_thread, args=(conn, identifier, msg))
            thread.start()

    @classmethod
    def send_to_conn(cls, conn, identifier, msg):
        """Starts a thread and sends the provided message to the socket provided"""
        thread = threading.Thread(target=cls.send_to_conn_thread, args=(conn, identifier, msg))
        thread.start()

    @classmethod
    def send_to_conn_thread(cls, conn, identifier, msg):
        """Do not call this directly"""
        message = (identifier + MSG_TYPE_SPLITTER + msg).encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        conn.sendall(send_length)
        conn.sendall(message)

    @classmethod
    def add_recv_function(cls, messageIdentifier : str, function : Callable[[socket.socket, str], None]):
        """Adds a function that will be called when a message with the provided prefix is recieved"""
        cls.recv_functions[messageIdentifier] = function