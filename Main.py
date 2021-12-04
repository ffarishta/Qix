import pygame
import random
from Display import Display
from Player import Player
from Sparx import Sparx
from Qix import Qix
from pygame.locals import *


def main():
    pygame.init()
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Qix")
    bond = (150, 150, 400, 400)
    boarder = pygame.Rect(bond)
    clock = pygame.time.Clock()

    running = True
    inPush = False
    temp_path = []
    temp_vertices = []
    current_vertices = [(150, 150), (549, 150), (549, 549), (150, 549)]  # All the vertices currently on screen
    startpoints = ()

    display = Display()
    player = Player()
    qix = Qix()
    qix.polygon.x = random.randint(170, 385)
    qix.polygon.y = random.randint(170, 385)
    sparx = Sparx()
    speed = 1
    sparx.polygon.centerx = 150
    sparx.polygon.centery = random.randint(155, 385)
    time = pygame.time.get_ticks()
    prevscrsurf = None
    lastKey3 = None
    sparxHit = False
    countBlack = 158276
    countBlue = 0
    countBlue1 = 0
    counter = 0

    while running:
        clock.tick(70)
        pressed_keys = pygame.key.get_pressed()
        liferemain = "Life: " + str(player.get_life())
        if qix.infilled(screen):
            qix.polygon.x = random.randint(170, 385)
            qix.polygon.y = random.randint(170, 385)

        for event in pygame.event.get():
            if event.type == KEYDOWN:      #If the player presses space, that causes a push
                if event.key == K_SPACE:
                    startpoints = (player.rect.centerx, player.rect.centery)
                    temp_vertices.append(startpoints)
                    inPush = True
                    lastKey3 = K_SPACE
                key = event.key

            elif event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), boarder, 1)

        for vertex in player.vertices:  # displays all completed objects
            for element in vertex:
                current_vertices.append(element)  # The new vertex that was created based on player movement, append that to the list of current vertices
                current_vertices = list(dict.fromkeys(current_vertices))
            if len(vertex) > 2:
                pygame.draw.polygon(screen, [0, 128, 128], vertex, 0)
        if counter == 1:

            # Calculate Claimed Area
            for pixel in range(150, 550):
                for pixel2 in range(150, 550):
                    if screen.get_at((pixel, pixel2)) != (0, 0, 0, 255):
                        countBlue1 += 1

            countBlue = countBlue1
            countBlue1 = 0
            counter = 0

        for path in player.paths:  # displays all completed paths; puts a border on objects
            if len(path) >= 2:
                pygame.draw.lines(screen, [255, 255, 255], False, path, 1)

                #Player cannot traverse across paths that have been covered by others
                for element in path:
                    if screen.get_at(((element[0] + 1), element[1])) == (0, 128, 128) and screen.get_at(((element[0] - 1), element[1])) == (0, 128, 128):
                        screen.set_at(element, (255,255,254))
                    elif screen.get_at(((element[0]), element[1] + 1)) == (0, 128, 128) and screen.get_at(((element[0]), element[1] - 1)) == (0, 128, 128):
                        screen.set_at(element, (255, 255, 254))

        if len(temp_path) > 2 and player.get_life() > 0:  # displays path we are currently in
            pygame.draw.lines(screen, [0, 255, 255], False, temp_path[0:-1], 1)

        scrsurf = screen.get_at((player.rect.centerx, player.rect.centery))

        if inPush:
            if (sparx.polygon.centerx, sparx.polygon.centery) == startpoints:   #Checks to see if sparx hits players line while in push
                sparxHit = True
                player.rect.center = startpoints
                temp_path = []
                temp_vertices = []

                player.lifeDecrease()

                # Find a white pixel to spawn the sparx enemy at
                for i in range(150, 549):
                    for j in range(150, 549):
                        if screen.get_at((i, j)) == (255, 255, 255, 255):
                            sparx.polygon.center = (i, j)

                if sparx.infilled(screen) == False:
                    sparx.polygon.centerx = 400
                    sparx.polygon.centery = random.randint(155, 385)
                    if sparx.infilled(screen) == False:
                        sparx.polygon.centerx = random.randint(155, 385)
                        sparx.polygon.centery = 150
                        if sparx.infilled(screen) == False:
                            sparx.polygon.centerx = random.randint(155, 385)
                            sparx.polygon.centery = 400

                inPush = False

                #checks to see if Qix collides with player, as long as player is in a push
        if player.coll(qix.polygon.centerx, qix.polygon.centery, player.rect.centerx, player.rect.centery) and screen.get_at((player.rect.centerx, player.rect.centery)) != (255,255,255,255):
            inPush = False
            player.rect.center = startpoints
            temp_path = []
            temp_vertices = []

        else:
            qix.move(screen, speed)

            #Checks if Qix colides with players push trail
        if screen.get_at((qix.polygon.centerx, qix.polygon.centery)) == (0, 255, 255):
            player.lifeDecrease()
            temp_path = []
            temp_vertices = []
            player.rect.center = startpoints
            inPush = False

            #Checks if sparx collides with player
        if (sparx.polygon.centerx, sparx.polygon.centery) == (player.rect.centerx, player.rect.centery):

            inPush = False
            player.lifeDecrease()
            temp_path = []
            temp_vertices = []

            # Find a white pixel to spawn the sparx enemy at
            for i in range(150, 549):
                for j in range(150, 549):
                    if screen.get_at((i, j)) == (255, 255, 255, 255):
                        sparx.polygon.center = (i, j)
                        break
                    break


        else:
            sparx.move(screen, speed)

            #Handles Qix movement on screen
        if pygame.time.get_ticks() >= time + 1000:
            qix.changedir()
            time = pygame.time.get_ticks()
        if inPush == False:
            player.move(screen, pressed_keys)

        if inPush and sparxHit == False:
                #Checks if player hits own trail in push
            if (player.rect.centerx, player.rect.centery) in temp_path and (player.rect.centerx, player.rect.centery) != \
                    temp_path[-1]:  # ABORT PUSH
                inPush = False
                player.rect.center = startpoints
                temp_path = []
                temp_vertices = []

                #When the player reaches an edge after a push
            if scrsurf == (255, 255, 255, 255) and prevscrsurf == (
                    0, 0, 0,255) and inPush and sparxHit is False and lastKey3 != K_SPACE:  #when we hit a white line in our push
                counter = 1
                inPush = False
                temp_vertices.append(player.rect.center)

                if len(temp_vertices) <= 2:
                    player.search(temp_vertices, temp_vertices[-1])
                if temp_vertices[0][1] != temp_vertices[-1][1] and temp_vertices[0][0] != temp_vertices[-1][0]:
                    player.search(temp_vertices, temp_vertices[-1])

                player.setVertices(temp_vertices)
                player.setPath(temp_path)
                temp_path = []
                temp_vertices = []

            else:
                player.push(screen, pressed_keys)
                player.setTempPath(temp_path)
                player.setTempVertex(temp_vertices, key)
            prevscrsurf = scrsurf

        if player.get_life() < 1:
            screen.blit(display.gameOver(), (250, 250))
        else:
                #Checks total percentage of claimed area to see if player wins
            if ((countBlue / countBlack) *100) > 75:
                screen.blit(display.winner(),(300,300))
                screen.blit(display.percentage(countBlue, countBlack), (300, 100))
            else:
                if screen.get_at((sparx.polygon.centerx, sparx.polygon.centery)) == (255, 255, 255, 255):
                    screen.blit(sparx.enemy, sparx.polygon)

                    #Checks if Sparx is in claimed area
                elif (sparx.polygon.centerx, sparx.polygon.centery) != startpoints:

                    #Find white pixel to spawn Sparx at
                    for i in range(150, 549):
                        for j in range(150, 549):
                            if screen.get_at((i, j)) == (255, 255, 255, 255):
                                sparx.polygon.center = (i, j)
                                break
                            break

                screen.blit(player.image, player.rect)
                screen.blit(display.Qiximage, (140, 100))
                if screen.get_at((qix.polygon.centerx, qix.polygon.centery)) != (0, 128, 128):
                    screen.blit(qix.enemy, qix.polygon)
                else:
                    # Find white pixel to spawn Qix at
                    for i in range(200, 500):
                        for j in range(200, 500):
                            if screen.get_at((i, j)) == (0, 0, 0):
                                qix.polygon.center = (i, j)
                                break
                screen.blit(display.life(liferemain), (500, 100))
                screen.blit(display.percentage(countBlue, countBlack), (300, 100))
                countBlue1 = 0

        sparxHit = False
        lastKey3 = None
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()