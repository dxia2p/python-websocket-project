import pygame
import clientcamera

class ClientBullet:
    bullets = []
    BULLET_RADIUS = 10
    def __init__(self, pos, vel, id) -> None:
        self.pos = pos
        self.velocity = vel
        self.id = id
        ClientBullet.bullets.append(self)
    
    @classmethod
    def update_all(cls, delta_time):
        for bullet in cls.bullets:
            bullet.pos += bullet.velocity * delta_time
            clientcamera.Camera.draw_circle(bullet.pos, cls.BULLET_RADIUS, "yellow")

    @classmethod
    def remove_at_id(cls, id):
        id_found = False
        for bullet in cls.bullets:
            if bullet.id == id:
                id_found = True
                cls.bullets.remove(bullet)
        
        if not id_found:
            print(f"Bullet id [{id}] not found!")
            