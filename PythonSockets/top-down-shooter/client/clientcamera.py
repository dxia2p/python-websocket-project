import pygame

class Camera:
    pos = pygame.Vector2(0, 0)
    size = pygame.Vector2(0, 0)
    screen = None

    @classmethod
    def initialize(cls, screen, size):
        cls.screen = screen
        cls.size = size

    @classmethod
    def draw_circle(cls, pos, radius, color):
        pygame.draw.circle(cls.screen, color, pos + pygame.Vector2(-cls.pos.x, cls.pos.y) + pygame.Vector2(cls.size.x / 2, cls.size.y / 2), radius)