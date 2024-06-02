import pygame
import clientnetworkhandler
import clientplayer
import json
import clientcamera
import clientbullet
import clientenemy

pygame.init()

screen = pygame.display.set_mode((700, 700))

pygame.display.set_caption("My Game")
running = True

handler = clientnetworkhandler.ClientNetworkHandler
handler.initialize()

WINDOW_SIZE_X = 700
WINDOW_SIZE_Y = 700

clientcamera.Camera.initialize(screen, pygame.Vector2(WINDOW_SIZE_X, WINDOW_SIZE_Y))

my_id = -1
players = {} # key: id of player, value : player object
BULLET_SPEED = 400

def on_player_moved(msg):
    player_move_data = json.loads(msg) # [id, {"x" : x, "y" : y}]
    players[player_move_data[0]].pos = pygame.Vector2(player_move_data[1]["x"], player_move_data[1]["y"])

handler.add_function("player_moved", on_player_moved)


def receive_all_players(msg): # This is only called at the start on a newly joined player
    players_list = json.loads(msg)

    for player in players_list:
        players[player[0]] = clientplayer.ClientPlayer(pygame.Vector2(player[1]["x"], player[1]["y"]))

handler.add_function("receive_all", receive_all_players)

def recieve_my_id(msg):
    global my_id
    my_id = int(msg)

handler.add_function("receive_my_id", recieve_my_id)


def on_player_added(msg):
    new_player_data = json.loads(msg)
    players[new_player_data[0]] = clientplayer.ClientPlayer(pygame.Vector2(new_player_data[1]["x"], new_player_data[1]["y"]))

handler.add_function("player_added", on_player_added)

def on_player_left(msg):
    id = json.loads(msg)[0]
    players.pop(id)

handler.add_function("player_left", on_player_left)

def on_player_shot(msg):
    data = json.loads(msg) # [{"x" : x, "y" : y}, {"x" : x, "y" : y}, id] First is the position to shoot from, second is direction
    pos = pygame.Vector2(data[0]["x"], data[0]["y"])
    vel = pygame.Vector2(data[1]["x"], data[1]["y"]) * BULLET_SPEED
    clientbullet.ClientBullet(pos, vel, data[2])

handler.add_function("player_shot", on_player_shot)

def on_bullet_destroyed(msg):
    id = int(msg)
    clientbullet.ClientBullet.remove_at_id(id)
    pass

handler.add_function("bullet_destroyed", on_bullet_destroyed)

def receive_all_enemies(msg):
    data = json.loads(msg)
    print(data)
    for enemy in data:
        clientenemy.ClientEnemy(enemy[0], pygame.Vector2(enemy[1]["x"], enemy[1]["y"]))

handler.add_function("receive_all_enemies", receive_all_enemies)

def on_enemy_spawned(msg):
    data = json.loads(msg) # [id, {"x" : x, "y" : y}]
    clientenemy.ClientEnemy(data[0], pygame.Vector2(data[1]["x"], data[1]["y"]))

handler.add_function("enemy_spawned", on_enemy_spawned)

clock = pygame.time.Clock()
lastInput = {"x" : 0, "y" : 0}
delta_time = 0
# ------------------------------- MAIN LOOP --------------------------------------
while running:

    screen.fill((255, 255, 255))

    events = pygame.event.get()

    input = {"x" : 0, "y" : 0}
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        input["x"] -= 1
    if keys[pygame.K_RIGHT]:
        input["x"] += 1
    if keys[pygame.K_DOWN]:
        input["y"] -= 1
    if keys[pygame.K_UP]:
        input["y"] += 1
    
    if input != lastInput:
        handler.send("move_input", json.dumps(input)) # i for input, this will tell the server that input data is being sent
    lastInput = input

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Tell the server that we want to shoot and provide the direction we are shooting in
                shoot_dir = (clientcamera.Camera.mouse_pos_to_world(pygame.mouse.get_pos()) - players[my_id].pos).normalize()
                send_dict = {"x" : shoot_dir.x, "y" : shoot_dir.y}
                handler.send("shoot_input", json.dumps(send_dict))

    if len(players) > 0:
        clientcamera.Camera.pos = pygame.Vector2(players[my_id].pos.x, players[my_id].pos.y)



    clientcamera.Camera.draw_circle(pygame.Vector2(0, 0), 20, "pink")

    # Draw grid lines to help the player visualize their movement
    grid_size = 30
    line_width = 1
    line_color = (175, 217, 237)

    if my_id != -1:
        player_pos = players[my_id].pos
        for i in range(int(player_pos.x - WINDOW_SIZE_X / 2 - player_pos.x % grid_size), int(player_pos.x + WINDOW_SIZE_X - player_pos.x % grid_size), grid_size): # draw the vertical lines
            clientcamera.Camera.draw_line(pygame.Vector2(i, player_pos.y - WINDOW_SIZE_X / 2), pygame.Vector2(i, player_pos.y + WINDOW_SIZE_X / 2), line_width, line_color)
        for i in range(int(player_pos.y - WINDOW_SIZE_Y / 2 - player_pos.y % grid_size), int(player_pos.y + WINDOW_SIZE_Y / 2 - player_pos.y % grid_size + grid_size), grid_size): # draw the horizontal lines
            clientcamera.Camera.draw_line(pygame.Vector2(player_pos.x - WINDOW_SIZE_Y / 2, i), pygame.Vector2(player_pos.x + WINDOW_SIZE_Y / 2, i), line_width, line_color)


    # Draw all the players
    for player_id in players:
        if player_id == my_id:
            clientcamera.Camera.draw_circle(players[player_id].pos, 15, "green")
        else:
            clientcamera.Camera.draw_circle(players[player_id].pos, 15, "blue")


    clientbullet.ClientBullet.update_all(delta_time)
    clientenemy.ClientEnemy.draw_all()

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000

    for event in events:
        if event.type == pygame.QUIT:
            running = False
handler.send("", "!DISCONNECT")
pygame.quit()