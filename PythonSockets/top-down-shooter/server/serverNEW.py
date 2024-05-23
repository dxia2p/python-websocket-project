import servernetworkhandler
import serverPlayer
import json
import time

networkHandler = servernetworkhandler.ServerNetworkHandler

PLAYER_MOVE_SPEED = 10
MSI = servernetworkhandler.MSG_SPLIT_IDENTIFIER
players = {}
playerInputs = {}

def client_added_callback(conn):

    # Give the new player all the existing players BEFORE the new player is created on the server to avoid duplicates
    all_players_json = []
    for player_id in players:
        all_players_json.append([player_id, {"x" : players[player_id].pos.x, "y" : players[player_id].pos.y}])
    networkHandler.send_to_conn(conn, "recieve_all" + MSI + json.dumps(all_players_json))

    players[conn] = serverPlayer.ServerPlayer()

    # Now send to all players that a new player has been added
    new_player_msg = json.dumps([players[conn].id, {"x" : players[conn].pos.x, "y" : players[conn].pos.y}])
    networkHandler.send_to_all(new_player_msg)
    

def client_removed_callback(conn):
    players.pop(conn)
    playerInputs.pop(conn)

networkHandler.initialize(client_added_callback=client_added_callback, client_removed_callback=client_removed_callback)


def onInput(conn, msg):
    input = json.loads(msg)
    playerInputs[conn] = input
    
networkHandler.add_recv_function("i", onInput)

# ------------------------- MAIN LOOP ----------------------

while True:
    for conn in playerInputs:
        players[conn].pos.x += playerInputs[conn]["x"]
        players[conn].pos.y += playerInputs[conn]["y"]

    for conn in players:
        msg = json.dumps([players[conn].id, {"x" : players[conn].pos.x, "y" : players[conn].pos.y}])
        networkHandler.send_to_all("move_player" + MSI + msg)

    clock = time.perf_counter() * 60 # CODE TO MAKE THIS LOOP RUN 60 TIMES A SECOND
    sleep = int(clock) + 1 - clock
    time.sleep(sleep)