import pygame
import time

class ServerPlayer:
    next_id = 0
    def __init__(self, pos=pygame.Vector2(0,0)) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.id = ServerPlayer.next_id
        ServerPlayer.next_id += 1