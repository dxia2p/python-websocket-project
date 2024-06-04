import servernetworkhandler
from serverplayer import ServerPlayer
import json
import time
import serverbullet
import servercolliders
import pygame
import serverenemy
import random
import math

ip = input("Enter IP, leave blank for default IP:")

handler = servernetworkhandler.ServerNetworkHandler

PLAYER_MOVE_SPEED = 200
BULLET_RADIUS = 7
BULLET_SPEED = 400

player_move_inputs = {}
player_shoot_inputs = {}

def client_added_callback(conn):

    # Give the new player all the existing players BEFORE the new player is created on the server to avoid duplicates
    all_players_json = []
    for player_conn in ServerPlayer.players:
        player = ServerPlayer.players[player_conn]
        all_players_json.append([player.id, {"x" : player.pos.x, "y" : player.pos.y}])

    handler.send_to_conn(conn, "receive_all", json.dumps(all_players_json))

    ServerPlayer.players[conn] = ServerPlayer(conn)
    player_move_inputs[conn] = pygame.Vector2(0, 0)
    player_shoot_inputs[conn] = pygame.Vector2(0, 0)
    handler.send_to_conn(conn, "receive_my_id", str(ServerPlayer.players[conn].id))

    # Now send to all players that a new player has been added
    new_player_msg = json.dumps([ServerPlayer.players[conn].id, {"x" : ServerPlayer.players[conn].pos.x, "y" : ServerPlayer.players[conn].pos.y}])
    handler.send_to_all("player_added", new_player_msg)

    # Send to the new player all the existing enemies
    send_enemies_message = []
    for enemy in serverenemy.ServerEnemy.enemies:
        send_enemies_message.append([enemy.id, {"x" : enemy.pos.x, "y" : enemy.pos.y}])
    handler.send_to_conn(conn, "receive_all_enemies", json.dumps(send_enemies_message))
    

def client_removed_callback(conn):
    handler.send_to_all_except_conn(conn, "player_left", json.dumps([ServerPlayer.players[conn].id]))
    for enemy in serverenemy.ServerEnemy.enemies:
        if enemy.target_pos == ServerPlayer.players[conn].pos:
            enemy.target_pos = None
    ServerPlayer.players.pop(conn)
    player_move_inputs.pop(conn)
    player_shoot_inputs.pop(conn)

# Start the server
if ip == "":
    handler.initialize(client_added_callback=client_added_callback, client_removed_callback=client_removed_callback)
else:
    handler.initialize(client_added_callback=client_added_callback, client_removed_callback=client_removed_callback, ip=ip)

def on_move_input(conn, msg):
    input = json.loads(msg)
    player_move_inputs[conn] = pygame.Vector2(input["x"], input["y"])
    
handler.add_recv_function("move_input", on_move_input)


def on_shoot_input(conn, msg):
    input_dirs = json.loads(msg)
    player_shoot_inputs[conn] = pygame.Vector2(input_dirs["x"], input_dirs["y"])

handler.add_recv_function("shoot_input", on_shoot_input)

# ------------------------- MAIN LOOP ----------------------
last_time = time.perf_counter()
delta_time = 0
start_spawn_enemies_delay = 3
spawn_enemies_delay = 1
while True:
    for conn in player_move_inputs.copy():
        if player_move_inputs[conn].x != 0 or player_move_inputs[conn].y != 0:
            move_dir = pygame.Vector2(player_move_inputs[conn].x, player_move_inputs[conn].y).normalize()
            ServerPlayer.players[conn].pos.x += move_dir.x * PLAYER_MOVE_SPEED * delta_time
            ServerPlayer.players[conn].pos.y += move_dir.y * PLAYER_MOVE_SPEED * delta_time

    for conn in ServerPlayer.players.copy(): # need to make a copy of the dictionary so that there is no error if a player joins while we are looping through the players dictionary
        msg = json.dumps([ServerPlayer.players[conn].id, {"x" : ServerPlayer.players[conn].pos.x, "y" : ServerPlayer.players[conn].pos.y}])
        handler.send_to_all("player_moved", msg)

    for conn in player_shoot_inputs.copy():
        if player_shoot_inputs[conn] != pygame.Vector2(0, 0): # This means the player wants to shoot
            shoot_dir = pygame.Vector2(player_shoot_inputs[conn].x, player_shoot_inputs[conn].y)
            bullet = serverbullet.ServerBullet(pygame.Vector2(ServerPlayer.players[conn].pos.x, ServerPlayer.players[conn].pos.y), pygame.Vector2(shoot_dir.x, shoot_dir.y) * BULLET_SPEED, BULLET_RADIUS)
            shoot_msg = [{"x" : ServerPlayer.players[conn].pos.x, "y" : ServerPlayer.players[conn].pos.y}, {"x" : shoot_dir.x, "y" : shoot_dir.y}, bullet.id]
            handler.send_to_all("player_shot", json.dumps(shoot_msg))
            player_shoot_inputs[conn] = pygame.Vector2(0, 0)

    if len(ServerPlayer.players) != 0:
        # Start spawning enemies
        if spawn_enemies_delay <= 0:
            rand_angle = random.random() * 2 * math.pi
            random_pos = pygame.Vector2(math.cos(rand_angle), math.sin(rand_angle)) * 1000
            serverenemy.ServerEnemy(random_pos, ServerPlayer.players)
            spawn_enemies_delay = start_spawn_enemies_delay
        else:
            spawn_enemies_delay -= delta_time
    
    serverbullet.ServerBullet.update_all_bullets(delta_time)
    
    servercolliders.CircleCollider.check_collision()
    servercolliders.CircleCollider.check_for_destroy()

    serverenemy.ServerEnemy.update_all(delta_time, ServerPlayer.players)
    # Put all logic above here -------------------------------------------

    clock = time.perf_counter() * 60 # CODE TO MAKE THIS LOOP RUN 60 TIMES A SECOND
    sleep = int(clock) + 1 - clock
    time.sleep(sleep / 60)

    delta_time = time.perf_counter() - last_time
    last_time = time.perf_counter()