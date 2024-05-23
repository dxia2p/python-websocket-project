import servernetworkhandler
import serverPlayer
import json
import time

networkHandler = servernetworkhandler.ServerNetworkHandler

PLAYER_MOVE_SPEED = 10
players = {}

def client_added_callback(conn):
    # Give the new player all the existing players BEFORE the new player is created on the server to avoid duplicates
    #networkHandler.send_to_conn(conn, "loadPlayers" + servernetworkhandler.MSG_SPLIT_IDENTIFIER + )

    # Send a message to all players saying that a player has been added

    players[conn] = serverPlayer.ServerPlayer()

def client_removed_callback(conn):
    players.pop(conn)

networkHandler.initialize(client_added_callback=client_added_callback, client_removed_callback=client_removed_callback)

playerInputs = {}
def onInput(conn, msg):
    input = json.loads(msg)
    playerInputs[conn] = input
    
networkHandler.add_recv_function("i", onInput)

# ------------------------- MAIN LOOP ----------------------

while True:

    for conn in playerInputs:
        players[conn].pos.x += playerInputs[conn]["x"]
        players[conn].pos.y += playerInputs[conn]["y"]

    #networkHandler.send_to_all("p" + servernetworkhandler.MSG_SPLIT_IDENTIFIER + )

    clock = time.perf_counter() * 60 # CODE TO MAKE THIS LOOP RUN 60 TIMES A SECOND
    sleep = int(clock) + 1 - clock
    time.sleep(sleep)