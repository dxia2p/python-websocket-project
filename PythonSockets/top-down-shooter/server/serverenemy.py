import utility
import pygame

class ServerEnemy:
    enemies = []
    MOVE_SPEED = 50
    def __init__(self, pos, players):
        self.pos = pos
        self.target_player = None
        shortest_dist = 10000000
        for player in players:
            dist = utility.vector2_dist(player.pos, self.pos)
            if dist < shortest_dist:
                self.target_player = player
                shortest_dist = dist
        

    @classmethod
    def update_all(cls, delta_time):
        for enemy in cls.enemies:
            if enemy.target_player == None:
                continue
            target_player_dir = enemy.target_player