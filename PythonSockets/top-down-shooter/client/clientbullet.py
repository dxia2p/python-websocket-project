import pygame
import clientcamera

class ClientBullet:
    bullets = []
    BULLET_RADIUS = 10
    def __init__(self, pos, vel) -> None:
        self.pos = pos
        self.velocity = vel
        ClientBullet.bullets.append(self)
    
    @classmethod
    def update_all(cls, delta_time):
        for bullet in cls.bullets:
            bullet.pos += bullet.velocity * delta_time
            clientcamera.Camera.draw_circle(bullet.pos, cls.BULLET_RADIUS, "yellow")

    