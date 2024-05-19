import pygame
import clientnetworkhandler
import json

pygame.init()

screen = pygame.display.set_mode((700, 700))

pygame.display.set_caption("My Game")
running = True

handler = clientnetworkhandler.ClientNetworkHandler
handler.initialize()

clock = pygame.time.Clock()
lastInput = {"x" : 0, "y" : 0}
while running:
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
        handler.send("i|" + json.dumps(input)) # i for input, this will tell the server that input data is being sent
    lastInput = input

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
handler.send("!DISCONNECT")
pygame.quit()