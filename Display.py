import pygame

class Display:
    def __init__(self):
        self.Qiximage = pygame.transform.scale(pygame.image.load('logo.png'), (100, 30))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 15)

        #Input: Amount of claimed pixels, Amount of total pixels in the field. Output: Text displaying the claimed percentage
    def percentage(self, countBlue, countBlack):
        percent = round((countBlue / countBlack) * 100, 1)
        percentage = "Percentage: " + str(percent) + "%"
        textsurface = self.myfont.render(percentage, False, (255, 255, 255))
        return textsurface

        #Input: Amount of lives remaining. Output: Text displaying amount of lives remaining
    def life(self,liferemain):
        textsurface = self.myfont.render(liferemain, False, (255, 255, 255))
        return textsurface

        #Input: N/A. Output: Text diplaying Gameover
    def gameOver(self):
        gameover = self.myfont.render('Game Over!', False, (255, 255, 255))
        return gameover

        # Input: N/A. Output: Text diplaying You win!
    def winner(self):
        winner = self.myfont.render("You Win!", False, (255, 255, 255))
        return winner
