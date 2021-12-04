import pygame
import random
from pygame.locals import *
dir=random.randint(1, 4)
boundary=(255,255,255)
filled=(0, 128, 128, 255)
class Qix(pygame.sprite.Sprite):
    def __init__(self):
        super(Qix, self).__init__()
        self.enemy = pygame.Surface((20, 20))
        self.enemy.fill((255, 0, 0))
        self.polygon = self.enemy.get_rect()

        #Input: Screen to be displayed on, Speed of enemy. Output: Side effect of Qix enemy movement
    def move(self,screen,speed):
        global dir
        screenenemy1 = screen.get_at((self.polygon.centerx - (5+speed), self.polygon.centery))
        screenenemy2 = screen.get_at((self.polygon.centerx + (5+speed), self.polygon.centery))
        screenenemy3 = screen.get_at((self.polygon.centerx, self.polygon.centery - (5+speed)))
        screenenemy4 = screen.get_at((self.polygon.centerx, self.polygon.centery + (5+speed)))
        if screenenemy1 == boundary:
            self.polygon.x = self.polygon.x + (15+speed)
            dir = 3
        if screenenemy2 == boundary:
            self.polygon.x = self.polygon.x - (15+speed)
            dir = 4
        if screenenemy3 == boundary :
            self.polygon.y = self.polygon.y + (15+speed)
            dir = 2
        if screenenemy4 == boundary :
            self.polygon.y = self.polygon.y - (15+speed)
            dir = 1
        if dir==1:
            self.polygon.move_ip(0, -speed)
        elif dir==2:
            self.polygon.move_ip(0, speed)
        elif dir==3:
            self.polygon.move_ip(speed, 0)
        else:
            self.polygon.move_ip(-speed, 0)

        #Input: N/A, Output: Random direction for Qix movement
    def changedir(self):
        global dir
        dir = random.randint(1, 4)
        return dir

        #Input: The screen. Output: Boolean value checking if in area claimed
    def infilled(self,screen):
        centreface=screen.get_at((self.polygon.centerx, self.polygon.centery))
        if centreface == filled :
            return True
        else:
            return False