import pygame
import math

def vector2_dist(vec1 : pygame.Vector2, vec2 : pygame.Vector2):
    return math.sqrt((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)