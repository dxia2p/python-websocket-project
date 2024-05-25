import servernetworkhandler
import serverPlayer
import json
import time

networkHandler = servernetworkhandler.ServerNetworkHandler

PLAYER_MOVE_SPEED = 100
players = {}
player_inputs = {}

def client_added_callback(conn):

    # Give the new player all the existing players BEFORE the new player is created on the server to avoid duplicates
    all_players_json = []
    for player_conn in players:
        player = players[player_conn]
        all_players_json.append([player.id, {"x" : player.pos.x, "y" : player.pos.y}])
    print(json.dumps(all_players_json))
    networkHandler.send_to_conn(conn, "receive_all", json.dumps(all_players_json))

    players[conn] = serverPlayer.ServerPlayer()
    player_inputs[conn] = {"x" : 0, "y" : 0}

    # Now send to all players that a new player has been added
    new_player_msg = json.dumps([players[conn].id, {"x" : players[conn].pos.x, "y" : players[conn].pos.y}])
    networkHandler.send_to_all("player_added", new_player_msg)
    

def client_removed_callback(conn):
    players.pop(conn)
    player_inputs.pop(conn)

networkHandler.initialize(client_added_callback=client_added_callback, client_removed_callback=client_removed_callback)


def onInput(conn, msg):
    input = json.loads(msg)
    player_inputs[conn] = input
    
networkHandler.add_recv_function("i", onInput)

# ------------------------- MAIN LOOP ----------------------
last_time = time.perf_counter()
delta_time = 0
while True:
    for conn in player_inputs:
        players[conn].pos.x += player_inputs[conn]["x"] * PLAYER_MOVE_SPEED * delta_time
        players[conn].pos.y -= player_inputs[conn]["y"] * PLAYER_MOVE_SPEED * delta_time

    for conn in players:
        msg = json.dumps([players[conn].id, {"x" : players[conn].pos.x, "y" : players[conn].pos.y}])
        networkHandler.send_to_all("move_player", msg)

    # Put all logic above here -------------------------------------------

    clock = time.perf_counter() * 60 # CODE TO MAKE THIS LOOP RUN 60 TIMES A SECOND
    sleep = int(clock) + 1 - clock
    time.sleep(sleep / 60)

    delta_time = time.perf_counter() - last_time
    last_time = time.perf_counter()