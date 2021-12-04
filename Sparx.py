import pygame
import random
from pygame.locals import *
dir=4
boundary=(255,255,255)
counter=1
class Sparx(pygame.sprite.Sprite):
    def __init__(self):
        super(Sparx, self).__init__()
        self.enemy = pygame.Surface((20, 20))
        self.enemy.fill((0, 0, 255))
        self.polygon = self.enemy.get_rect()

        # Input: Screen to be displayed on, Speed of enemy. Output: Side effect of Sparx enemy movement
    def move(self,screen,speed):
        global counter
        screensparx = screen.get_at((self.polygon.centerx, self.polygon.centery))
        screensparx1 = screen.get_at((self.polygon.centerx - 1, self.polygon.centery))
        screensparx2 = screen.get_at((self.polygon.centerx + 1, self.polygon.centery))
        screensparx3 = screen.get_at((self.polygon.centerx, self.polygon.centery - 1))
        screensparx4 = screen.get_at((self.polygon.centerx, self.polygon.centery + 1))

        dir = self.getdir()
        if screensparx == boundary:
            if dir == 1:
                self.polygon.move_ip(-speed, 0)
                if screensparx3 == boundary:
                    if screensparx4 ==boundary:
                        self.polygon.centery = self.polygon.centery + 1
                        self.polygon.centerx = self.polygon.centerx + 1
                        self.changedir(4)
                    else:
                        self.polygon.centery = self.polygon.centery - 1
                        self.polygon.centerx = self.polygon.centerx + 1
                        self.changedir(3)

                elif  screensparx4 == boundary:
                        self.polygon.centery = self.polygon.centery + 1
                        self.polygon.centerx = self.polygon.centerx + 1
                        self.changedir(4)

            if dir == 2:
                self.polygon.move_ip(speed, 0)
                if  screensparx3 == boundary:
                    self.polygon.centery = self.polygon.centery - 1
                    self.polygon.centerx = self.polygon.centerx - 1
                    self.changedir(3)
                elif  screensparx4 == boundary:
                    if screensparx3 == boundary:
                        self.polygon.centery = self.polygon.centery - 1
                        self.polygon.centerx = self.polygon.centerx - 1
                        self.changedir(3)
                    else:
                        self.polygon.centery = self.polygon.centery + 1
                        self.polygon.centerx = self.polygon.centerx - 1
                        self.changedir(4)

            if dir == 3:
                self.polygon.move_ip(0, -speed)
                if screensparx1 == boundary :
                    self.polygon.centerx = self.polygon.centerx - 1
                    self.polygon.centery = self.polygon.centery + 1
                    self.changedir(1)

                elif screensparx2 == boundary :
                    if screensparx1 == boundary:
                        self.polygon.centerx = self.polygon.centerx - 1
                        self.polygon.centery = self.polygon.centery + 1
                        self.changedir(1)
                    else:
                        self.polygon.centerx = self.polygon.centerx + 1
                        self.polygon.centery = self.polygon.centery + 1
                        self.changedir(2)

            if dir == 4:
                self.polygon.move_ip(0, speed)
                if screensparx1 == boundary :
                    if screensparx2 == boundary:
                        self.polygon.centerx = self.polygon.centerx + 1
                        self.polygon.centery = self.polygon.centery - 1
                        self.changedir(2)
                    else:
                        self.polygon.centerx = self.polygon.centerx - 1
                        self.polygon.centery = self.polygon.centery - 1
                        self.changedir(1)

                elif screensparx2 == boundary:
                    self.polygon.centerx = self.polygon.centerx + 1
                    self.polygon.centery = self.polygon.centery - 1
                    self.changedir(2)

        # Input: N/A, Output: Random direction for Sparx movement
    def changedir(self,change):
        global dir
        dir=change
        return dir

        # Input: N/A, Output: Direction Sparx is moving
    def getdir(self):
        return dir

        # Input: The screen. Output: Boolean value checking if in area claimed
    def infilled(self, screen):
        centreface = screen.get_at((self.polygon.centerx, self.polygon.centery))
        if centreface == boundary:

            return True
        else:
            return False