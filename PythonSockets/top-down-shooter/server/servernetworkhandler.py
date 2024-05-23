import socket
import threading
from typing import Callable

BUFFER_SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_SPLIT_IDENTIFIER = '|'

class ServerNetworkHandler:
    port = -1
    ip = ""
    server = None

    recv_functions = {}
    client_added_callback = None

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
            cls.client_added_callback(conn)
            cls.clients.append(conn)
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

    @classmethod
    def handle_client(cls, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected: # LOGIC FOR RECIEVING DATA GOES HERE

            msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            split_msg = msg.split(MSG_SPLIT_IDENTIFIER, 1) # All messages should have this character after the identifier for the data in the message
            print(msg)
            if split_msg[0] in cls.recv_functions:
                cls.recv_functions[split_msg[0]](conn, split_msg[1])

        cls.client_removed_callback(conn)
        conn.close()

    @classmethod
    def send_to_all(cls, msg):
        """Starts a thread and sens the provided message to all sockets connected to this server"""
        thread = threading.Thread(target=cls.send_to_all_thread, args=(msg,))
        thread.start()

    @classmethod
    def send_to_all_thread(cls, msg):
        """Do not call this directly"""
        for client in cls.clients:
            message = msg.encode(FORMAT)
            client.send(message)

    @classmethod
    def send_to_conn(cls, conn, msg):
        """Starts a thread and sends the provided message to the socket provided"""
        thread = threading.Thread(target=cls.send_to_conn_thread, args=(conn, msg))

    @classmethod
    def send_to_conn_thread(cls, conn, msg):
        """Do not call this directly"""
        conn.send(msg.encode(FORMAT))

    @classmethod
    def add_recv_function(cls, messageIdentifier : str, function : Callable[[socket.socket, str], None]):
        """Adds a function that will be called when a message with the provided prefix is recieved"""
        cls.recv_functions[messageIdentifier] = function