from typing import Callable
import pygame
import math
import servercolliders
import servernetworkhandler

class ServerBullet:
    server_bullets = []
    next_id = 0

    def bullet_hit(self, other_collider):
        if other_collider.tag == "bullet":
            return
        self.destroy_self()
        self.circle_collider.destroy_self()
        servernetworkhandler.ServerNetworkHandler.send_to_all("bullet_destroyed", str(self.id))

    def __init__(self, pos, velocity, radius) -> None:
        self.pos = pos
        self.radius = radius
        self.velocity = velocity
        self.circle_collider = servercolliders.CircleCollider(pos, radius, "bullet", self.bullet_hit)
        self.id = ServerBullet.next_id
        ServerBullet.next_id += 1
        ServerBullet.server_bullets.append(self)

    @classmethod
    def update_all_bodies(cls, delta_time): # This function can be moved to a parent class later
        for body in cls.server_bullets:
            body.pos += body.velocity * delta_time

    def destroy_self(self):
        """Removes this collider from the list of server_bullets"""
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        ServerBullet.server_bullets.remove(self)
