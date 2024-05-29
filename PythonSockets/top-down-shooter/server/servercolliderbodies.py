from typing import Callable
import pygame
import math

def vector2_dist(vec1 : pygame.Vector2, vec2 : pygame.Vector2):
    return math.sqrt((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)

class CircleBody:
    collider_bodies = []
    def __init__(self, pos, velocity, radius, on_collision_func) -> None:
        self.pos = pos
        self.radius = radius
        self.velocity = velocity
        self.on_collision_func = on_collision_func
        CircleBody.collider_bodies.append(self)

    @classmethod
    def update_all_bodies(cls): # This function can be moved to a parent class later
        for body in cls.collider_bodies:
            body.pos += body.velocity

    @classmethod
    def check_collisions(cls): # This function can be moved to a parent class later
        """Call this every frame to detect collisions"""
        for i in range(len(cls.collider_bodies)):
            for j in range(i + 1, len(cls.collider_bodies)):
                if vector2_dist(cls.collider_bodies[i].pos, cls.collider_bodies[j].pos) < (cls.collider_bodies[i].radius + cls.collider_bodies[j].radius):
                    cls.collider_bodies[i].on_collision_func()
                    cls.collider_bodies[j].on_collision_func()

    def destroy_self(self):
        """Removes this collider from the list of collider_bodies"""
        CircleBody.collider_bodies.remove(self)
