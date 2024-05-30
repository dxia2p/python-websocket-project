from typing import Callable
import pygame
import math
import servercolliders

class ServerBullet:
    server_bullets = []

    def bullet_hit(self):
        self.destroy_self()
        self.circle_collider.destroy_self()

    def __init__(self, pos, velocity, radius) -> None:
        self.pos = pos
        self.radius = radius
        self.velocity = velocity
        self.circle_collider = servercolliders.CircleCollider(pos, radius, self.bullet_hit)
        ServerBullet.server_bullets.append(self)

    @classmethod
    def update_all_bodies(cls, delta_time): # This function can be moved to a parent class later
        for body in cls.server_bullets:
            body.pos += body.velocity * delta_time

    def destroy_self(self):
        """Removes this collider from the list of server_bullets"""
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        ServerBullet.server_bullets.remove(self)
