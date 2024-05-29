from typing import Callable
import pygame
import math

def vector2_dist(vec1 : pygame.Vector2, vec2 : pygame.Vector2):
    return math.sqrt((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)

class CircleBody:
    colliders = []
    def __init__(self, pos, radius, on_collision_func) -> None:
        self.pos = pos
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)
        self.on_collision_func = on_collision_func

    @classmethod
    def check_collisions(cls):
        """Call this every frame to detect collisions"""
        for i in range(len(cls.colliders)):
            for j in range(i, len(cls.colliders)):
                if vector2_dist(cls.colliders[i], cls.colliders[j]) < (cls.colliders[i].radius + cls.colliders[j].radius):
                    cls.colliders[i].on_collision_func()
                    cls.colliders[j].on_collision_func()

    def destroy_self(self):
        """Removes this collider from the list of colliders"""
        CircleBody.colliders.remove(self)
