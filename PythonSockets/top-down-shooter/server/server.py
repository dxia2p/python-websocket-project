import threading
import socket
import serverPlayer
import time
import json

HEADER = 64
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.settimeout(1.0)

players = []
connections = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected: # LOGIC FOR RECIEVING DATA GOES HERE
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: # check if message is none
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if(msg == DISCONNECT_MESSAGE):
                connected = False
            print(f"[{addr}] {msg}")
            
            if msg[0] == 'i':
                pass

    connections.remove(conn)
    conn.close()

def send_to_all(msg):
    for c in connections:
        c.send()

def main_game_loop(): # this is for game logic

    while True:
        for p in players:
            outputList = []
            outputList.append(p.id, p.pos)
            msg = "m" + json.dumps(outputList)
            send_to_all(msg)
            pass
        clock = time.perf_counter() * 60
        sleep = int(clock) + 1 - clock
        time.sleep(sleep / 60)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    main_loop_thread = threading.Thread(target=main_game_loop)
    main_loop_thread.daemon = True
    main_loop_thread.start()
    while True:
        try: # Handling new clients here
            conn, addr = server.accept()
            players[addr] = serverPlayer.Player(time.time)
            connections.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr)) # each client is connected on a new thread
            thread.daemon = True
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except IOError as msg: # I have to write this stupid stuff to let me exit with keyboard interrupt
            try:
                print(msg)
                continue
            except KeyboardInterrupt:
                print("Keyboard Interrupt, exiting")
                break
        except KeyboardInterrupt:
            print("Keyboard Interrupt, exiting")
            break

    server.close()


print("[STARTING] server is starting...")
start()