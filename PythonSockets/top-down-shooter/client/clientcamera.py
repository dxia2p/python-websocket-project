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
        pygame.draw.circle(cls.screen, color, pygame.Vector2(pos.x, -pos.y) + pygame.Vector2(-cls.pos.x, cls.pos.y) + pygame.Vector2(cls.size.x / 2, cls.size.y / 2), radius)

    @classmethod
    def draw_line(cls, start, end, width, color):
        start = pygame.Vector2(start.x, -start.y)
        end = pygame.Vector2(end.x, -end.y)
        pygame.draw.line(cls.screen, color, start + pygame.Vector2(-Camera.pos.x, Camera.pos.y) + pygame.Vector2(Camera.size.x / 2, Camera.size.y / 2), end + pygame.Vector2(-Camera.pos.x, Camera.pos.y) + pygame.Vector2(Camera.size.x / 2, Camera.size.y / 2), width)

    @classmethod
    def mouse_pos_to_world(cls, mouse_pos : pygame.Vector2) -> pygame.Vector2:
        """Returns the position of the mouse in world coordinates"""
        mouse_pos += pygame.Vector2(cls.pos.x, -cls.pos.y)
        mouse_pos += pygame.Vector2(-cls.size.x / 2, -cls.size.y / 2)
        mouse_pos = pygame.Vector2(mouse_pos.x, -mouse_pos.y)
        return mouse_pos