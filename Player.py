import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.life = 5
        self.image = pygame.transform.scale(pygame.image.load('m.png'), (25, 25))
        self.surf = pygame.Surface((25, 25))
        self.rect = self.surf.get_rect()
        self.rect.centerx = 350
        self.rect.centery = 549
        self.paths = []
        self.vertices = []
        self.prevKey = None
        self.keycount = sum(pygame.key.get_pressed())


    def move(self, screen, pressed_keys):
        """
        Paramenters:
        - Pygame object screen: screen of the game 
        - List pressed_keys: a list of all the keys pressed 

        Moves player within the restricted white boundaries of the field using the arrow keys  
        """
        scrsurf1 = screen.get_at((self.rect.centerx - 1, self.rect.centery))  # colour of left pixel
        scrsurf2 = screen.get_at((self.rect.centerx + 1, self.rect.centery))  # colour of right pixel 
        scrsurf3 = screen.get_at((self.rect.centerx, self.rect.centery - 1))  # colour of top pixel
        scrsurf4 = screen.get_at((self.rect.centerx, self.rect.centery + 1))  # color of bottom pixel 

        #check if the player can move to the directed pixel 
        if pressed_keys[K_UP] and scrsurf3 == (255, 255, 255, 255):
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN] and scrsurf4 == (255, 255, 255, 255):
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT] and scrsurf1 == (255, 255, 255, 255):
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT] and scrsurf2 == (255, 255, 255, 255):
            self.rect.move_ip(1, 0)

    def push(self, screen, pressed_keys):
        """
        Paramenters:
        - pygame object screen: screen of the game 
        - List pressed_keys: a list of all the keys pressed 

         Allows the player to move out of the boundaries into the field and create an incursion
        """
        
        if sum(pressed_keys) - self.keycount == 1: # allows only one key to be pushed 
            scrsurf1 = screen.get_at((self.rect.centerx - 1, self.rect.centery))  # colour of left pixel
            scrsurf2 = screen.get_at((self.rect.centerx + 1, self.rect.centery))  # colour of right pixel
            scrsurf3 = screen.get_at((self.rect.centerx, self.rect.centery - 1))  # colour of top pixel
            scrsurf4 = screen.get_at((self.rect.centerx, self.rect.centery + 1))  # color of bottom pixel 

            #conditions to check if push is wihin the feild 
            if pressed_keys[K_UP] and self.rect.centery > 150 and scrsurf3 != (0, 128, 128, 255):
                self.rect.move_ip(0, -1)

            if pressed_keys[K_DOWN] and self.rect.centery < 550 and scrsurf4 != (0, 128, 128, 255):
                self.rect.move_ip(0, 1)

            if pressed_keys[K_LEFT] and self.rect.centerx > 150 and scrsurf1 != (0, 128, 128, 255):
                self.rect.move_ip(-1, 0)

            if pressed_keys[K_RIGHT] and self.rect.centerx < 550 and scrsurf2 != (0, 128, 128, 255):
                self.rect.move_ip(1, 0)

    def setTempPath(self, temp):
        """
        Parameters:
        - List temp: list of tuples representing pixels within the path of the push  

        Adds pixel to the list of the path
        """
        if self.rect.center not in temp:
            temp.append(self.rect.center)

    def setTempVertex(self, temp, key):
        """
        Parameters:
        - List temp: list of vertices of current push  

        Adds vertex to the list of vertices of the current push
        """
        if key != self.prevKey and self.rect.center not in temp and (
                key or self.prevKey) != pygame.K_SPACE:  # do not duplicate vertex if same key is pressed again
            temp.append(self.rect.center)
            self.prevKey = key

    def setPath(self, temp):
        """
        Parameters:
        - List temp: list of tuples representing pixels within the path of the push  

        Adds list of pixels into the list of lines  
        """
        self.paths.append(temp)

    def setVertices(self, temp):
        """
        Parameters:
        - List temp: list of vertices of current push  

        Adds list of vertices into the the list of all pushes  
        """
        self.vertices.append(temp)

    def search(self, temp, last):
        """
        Parameters:
        - List temp: list of vertices of current push
        - Tuple last: the coordantes of the the last vertex

        Finds all the missing vertices   
        """
        x = [(150, 150), (549, 150), (549, 549), (150, 549)]
        vert = self.vertices.copy()
        sorted_temp_x = sorted(temp, key=lambda x: x[0], reverse=True)
        sorted_temp_y = sorted(temp, key=lambda x: x[1], reverse=True)
        max_x, max_y = sorted_temp_x[0][0], sorted_temp_y[0][1]
        min_x, min_y = sorted_temp_x[-1][0], sorted_temp_y[-1][1]
        
        found = False
        first = temp[0]

        if len(temp) == 2:
            if first[0] == (150 or 549) and last[0] == (549 or 150):
                if last[1] > 279:
                    temp += [(549, 549), (150, 549)]
                    # return
                else:
                    temp += [(549, 150), (150, 150)]
                    # return
            if first[1] == (549 or 150) and last[1] == (150 or 150):
                if last[0] < 279:
                    temp += [(150, 150), (150, 549)]
                    # return
                else:
                    temp += [(549, 150), (549, 549)]
                    # return

        x = [(150, 150), (549, 150), (549, 549), (150, 549)]
        for nextvert in x:
            if last[0] == nextvert[0] or last[1] == nextvert[1]:
                if ((min_x <= nextvert[0] <= max_x) and (min_y <= nextvert[1] <= max_y)):
                    temp.append(nextvert)
                    last = nextvert

        for i in range(len(vert)):
            nextvert = vert[i]
            for x in range(len(nextvert)):
                if last[0] == nextvert[x][0] or last[1] == nextvert[x][1]:
                    if ((min_x <= nextvert[x][0] <= max_x) and (min_y <= nextvert[x][1] <= max_y)) or found == True:
                        temp.append(nextvert[x])
                        last = nextvert[x]
                        found = True
                    if len(temp) <= 2:
                        temp.append(nextvert[x])
                        last = nextvert[x]
                    if first[0] == nextvert[x][0] or first[1] == nextvert[x][1]:
                        break

    def get_life(self):
        """
        Parameters: N/A  

        Returns player life  
        """
        return self.life

    def coll(self, x1, y1, x2, y2):
        """
        Returns true if collision is found at certain point   
        """
        if abs(x1 - x2) <= 15 and abs(y1 - y2) <= 15:
            self.lifeDecrease()
            return True

    def lifeDecrease(self):
        """
        Parameters: N/A  

        reduces player life 
        """
        self.life = self.life - 1
