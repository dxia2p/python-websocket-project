import pygame
import time
import servercolliders
import socket
import servernetworkhandler

class ServerPlayer:
    next_id = 0
    players = {}
    def on_collision_func(self, other_collider):
        if other_collider.tag == "enemy":
            #ServerPlayer.players.pop(self.conn)
            self.collider.destroy_self()
            servernetworkhandler.ServerNetworkHandler.send_to_conn(self.conn, "you_died", "haha")

    def __init__(self, conn, pos=pygame.Vector2(0,0)) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.id = ServerPlayer.next_id
        ServerPlayer.next_id += 1
        self.collider = servercolliders.CircleCollider(self.pos, 15, "player", self.on_collision_func)
        ServerPlayer.players[conn] = self
        self.conn = conn