import utility
import pygame
import servernetworkhandler
import json
import servercolliders

class ServerEnemy:
    enemies = []
    MOVE_SPEED = 50
    next_id = 0

    def destroy_self(self):
        ServerEnemy.enemies.remove(self)
        self.collider.destroy_self()
        servernetworkhandler.ServerNetworkHandler.send_to_all("enemy_died", str(self.id))

    def on_collide(self, other_collider):
        if other_collider.tag == "bullet":
            self.destroy_self()
        elif other_collider.tag == "player":
            self.target_pos = None

    def __init__(self, pos, players):
        self.pos = pos
        self.target_pos = None
        shortest_dist = 10000000
        for player_conn in players:
            dist = utility.vector2_dist(players[player_conn].pos, self.pos)
            if dist < shortest_dist:
                self.target_pos = players[player_conn].pos
                shortest_dist = dist
        self.id = ServerEnemy.next_id
        self.collider = servercolliders.CircleCollider(self.pos, 20, "enemy", self.on_collide) 
        ServerEnemy.next_id += 1
        send_msg = json.dumps([self.id, {"x" : self.pos.x, "y" : self.pos.y}])
        servernetworkhandler.ServerNetworkHandler.send_to_all("enemy_spawned", send_msg)
        ServerEnemy.enemies.append(self)
        

    @classmethod
    def update_all(cls, delta_time, players):
        data_to_send = []
        for enemy in cls.enemies:
            if enemy.target_pos == None:
                shortest_dist = 1000000
                for player_conn in players:
                    dist = utility.vector2_dist(players[player_conn].pos, enemy.pos)
                    if dist < shortest_dist:
                        enemy.target_pos = players[player_conn].pos
                        shortest_dist = dist
            else:
                target_player_dir = (enemy.target_pos - enemy.pos).normalize()
                enemy.pos += delta_time * target_player_dir * ServerEnemy.MOVE_SPEED
                data_to_send.append([enemy.id, {"x" : enemy.pos.x, "y" : enemy.pos.y}])
            
        servernetworkhandler.ServerNetworkHandler.send_to_all("enemy_moved", json.dumps(data_to_send))