import socket
import pygame

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

class NetworkHandler:
    port = -1
    ip = ""
    client = None

    @staticmethod
    def initialize(ip = socket.gethostbyname(socket.gethostname()), port = 6969):
        NetworkHandler.ip = ip
        NetworkHandler.port = port
        NetworkHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        NetworkHandler.client.connect((NetworkHandler.ip, NetworkHandler.port))


    def send(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        NetworkHandler.client.send(send_length)
        NetworkHandler.client.send(message)

    def recv(outputFunc):
        pass
