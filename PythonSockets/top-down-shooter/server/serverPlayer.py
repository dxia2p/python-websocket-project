import pygame
import time

class Player:
    def __init__(self, id, pos=pygame.Vector2(0,0)) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.id = id