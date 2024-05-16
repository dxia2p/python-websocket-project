import pygame
import networkHandler
import json

pygame.init()

screen = pygame.display.set_mode((700, 700))

pygame.display.set_caption("My Game")
running = True

handler = networkHandler.NetworkHandler
handler.initialize()

clock = pygame.time.Clock()

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
    
    if input != {"x" : 0, "y" : 0}:
        handler.send("i" + json.dumps(input)) # i for input, this will tell the server that input data is being sent

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()