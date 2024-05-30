import pygame
import math

def vector2_dist(vec1 : pygame.Vector2, vec2 : pygame.Vector2):
    return math.sqrt((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)

class CircleCollider: # can make a base class collider and inherit from that in the future, but for now only need circle class
    colliders = []
    colliders_to_destroy = []
    def __init__(self, pos, radius, on_collision_func) -> None:
        self.pos = pos
        self.radius = radius
        self.on_collision_func = on_collision_func
        CircleCollider.colliders.append(self)
    
    @classmethod
    def check_collision(cls):
        """Call this every frame to detect collisions"""
        for i in range(len(cls.colliders)):
            for j in range(i, len(cls.colliders)):
                if i == j:
                    continue
                if vector2_dist(cls.colliders[i].pos, cls.colliders[j].pos) < (cls.colliders[i].radius + cls.colliders[j].radius):
                    cls.colliders[i].on_collision_func()
                    cls.colliders[j].on_collision_func()

    @classmethod
    def check_for_destroy(cls):
        for collider in cls.colliders_to_destroy:
            CircleCollider.colliders.remove(collider)
        cls.colliders_to_destroy = []

    def destroy_self(self):
        CircleCollider.colliders_to_destroy.append(self) # queue up this collider for destruction after all the collision logic is finished