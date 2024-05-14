import websockets
import asyncio

PORT = 6969

print("Starteed server and its listening on port " + str(PORT))

async def echo(websocket, path):
    print("A client just connected")
    async for message in websocket:
        print("Recieved message from client: " + message)
        await websocket.send("PONG:" + message)


start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()