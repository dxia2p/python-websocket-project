import utility
import pygame
import servernetworkhandler
import json

class ServerEnemy:
    enemies = []
    MOVE_SPEED = 50
    next_id = 0
    def __init__(self, pos, players):
        self.pos = pos
        self.target_player = None
        shortest_dist = 10000000
        for player in players:
            dist = utility.vector2_dist(player.pos, self.pos)
            if dist < shortest_dist:
                self.target_player = player
                shortest_dist = dist
        self.id = ServerEnemy.next_id
        ServerEnemy.next_id += 1
        send_msg = json.dumps([self.id, {"x" : self.pos.x, "y" : self.pos.y}])
        servernetworkhandler.ServerNetworkHandler.send_to_all("enemy_spawned", send_msg)
        ServerEnemy.enemies.append(self)
        

    @classmethod
    def update_all(cls, delta_time):
        for enemy in cls.enemies:
            if enemy.target_player == None:
                continue
            target_player_dir = (enemy.target_player.pos - enemy.pos).normalize()
            enemy.pos += delta_time * target_player_dir * ServerEnemy.MOVE_SPEED
