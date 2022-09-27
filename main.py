import pygame
from pygame.locals import *
import os
import math
import noise
from mainmenu import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREENWIDTH = 1000
SCREENHEIGHT = 406


WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('platformer')


# draw stuff
BG_img = pygame.image.load(os.path.join('Assets', 'BG.png'))
BG_width = BG_img.get_width()


# def game variables

# math.ceil rounds number up, tile width calculates the number of tiles needed to be blitted to fill screen
tile_width = math.ceil(SCREENWIDTH / BG_width)



class player():
    def __init__(self, x,y):
        pimg = pygame.image.load(os.path.join('Assets', 'player.jpg'))
        self.image = pygame.transform.scale(pimg, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.grav = 0



    def movement(self):

        dx = 0 # when key is pressed, shows the change (delta)
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.grav = -15 # neg value increase y coord
        if keys[pygame.K_a]:
            dx -= 5
        if keys [pygame.K_d]:
            dx += 5


        self.grav += 1
        if self.grav > 10: # if y >10 then it gets capped and player starts falling

            self.grav = 10

        dy += self.grav


        #updating coords
        self.rect.x += dx
        self.rect.y += dy


        WIN.blit(self.image,self.rect)


player = player(100,300)


run = True
while run:

    clock.tick(FPS)

    # blit imgs
    for i in range(0, tile_width):
        WIN.blit(BG_img, (i * BG_width, 0))

    player.movement()

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()

