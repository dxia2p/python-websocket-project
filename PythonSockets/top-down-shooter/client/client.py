import pygame
import clientnetworkhandler
import clientplayer
import json
import clientcamera

pygame.init()

screen = pygame.display.set_mode((700, 700))

pygame.display.set_caption("My Game")
running = True

handler = clientnetworkhandler.ClientNetworkHandler
handler.initialize()

clientcamera.Camera.initialize(screen, pygame.Vector2(700, 700))

players = {} # key: id of player, value : player object

def move_player(msg):
    player_move_data = json.loads(msg) # [id, {"x" : x, "y" : y}]
    players[player_move_data[0]].pos = pygame.Vector2(player_move_data[1]["x"], player_move_data[1]["y"])

handler.add_function("move_player", move_player)

def receive_all_players(msg): # This is only called at the start on a newly joined player
    players_list = json.loads(msg)

    for player in players_list:
        players[player[0]] = clientplayer.ClientPlayer(pygame.Vector2(player[1]["x"], player[1]["y"]))

handler.add_function("receive_all", receive_all_players)

def player_added(msg):
    new_player_data = json.loads(msg)
    players[new_player_data[0]] = clientplayer.ClientPlayer(pygame.Vector2(new_player_data[1]["x"], new_player_data[1]["y"]))
    pass

handler.add_function("player_added", player_added)

clock = pygame.time.Clock()
lastInput = {"x" : 0, "y" : 0}
# ------------------------------- MAIN LOOP --------------------------------------
while running:

    screen.fill((0, 0, 0))

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
        handler.send("i", json.dumps(input)) # i for input, this will tell the server that input data is being sent
    lastInput = input

    # Draw all the players
    for player_id in players:
        clientcamera.Camera.draw_circle(players[player_id].pos, 10, "white")

    pygame.display.flip()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
handler.send("", "!DISCONNECT")
pygame.quit()