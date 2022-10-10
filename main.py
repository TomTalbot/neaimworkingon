import pygame
import os
import math
import pygame_menu
import noise


pygame.init()
pygame.display.init()

global TEMPRES


clock = pygame.time.Clock()
FPS = 60

SCREENWIDTH, SCREENHEIGHT = 1000, 406


WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('platformer')


# draw stuff
BG_img = pygame.image.load(os.path.join('Assets', 'BG.png'))
BG_width = BG_img.get_width()
BG_height = BG_img.get_height()

dirt_image = pygame.image.load(os.path.join('Assets', 'dirt.png'))
grass_image = pygame.image.load(os.path.join('Assets', 'grass.png'))
TILE_SIZE = grass_image.get_width()


# math.ceil rounds number up, tile width calculates the number of tiles needed to be blitted to fill screen
tile_width = math.ceil(SCREENWIDTH / BG_width)
tile_height = math.ceil(SCREENHEIGHT / BG_height)


class Player:
    def __init__(self, x, y):
        pimg = pygame.image.load(os.path.join('Assets', 'player.png'))
        self.image = pygame.transform.scale(pimg, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.grav = 0

    def movement(self):

        dx = 0  # when key is pressed, shows the change (delta)
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.grav = -15  # neg value increase y coord
        if keys[pygame.K_a]:
            dx -= 5
        if keys[pygame.K_d]:
            dx += 5

        self.grav += 1

        if self.grav > 10:  # if y >10 then it gets capped and player starts falling

            self.grav = 10

        dy += self.grav

        # updating coords
        self.rect.x += dx
        self.rect.y += dy

        WIN.blit(self.image, self.rect)


player = Player(100, 300)


def game():

    run = True
    while run:

        clock.tick(FPS)

        # blit imgs
        for i in range(0, tile_width):
            WIN.blit(BG_img, (i * BG_width, 0))
        for i in range(0, tile_height):
            WIN.blit(BG_img, (i * BG_height, 0))

        player.movement()

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

# menu shit


def settings():

    settings = pygame_menu.Menu('Settings', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    settings.add.button('Audio', audio)
    settings.add.button('Video', video)
    settings.add.button('Back', mainMenu)
    settings.mainloop(WIN)


def audio():

    audio = pygame_menu.Menu('Audio', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    audio.add.button('Back', settings)
    audio.mainloop(WIN)


def video():

    video = pygame_menu.Menu('Video', 1000, 406, theme=pygame_menu.themes.THEME_DARK)

    # all example resolutions

    video.add.selector('Screen Dimensions : ', [('1366x768', 1), ('1280x1024', 2), ('800x600', 3)],
                       onchange=temp_resolution, selector_id='set_resolution')

    video.add.button('Apply', resolution)
    video.add.button('Back', settings)
    video.mainloop(WIN)

# window wont resize if the res chosen first is in the list without scrolling breaks code for some reason?
def temp_resolution(value: tuple[any, any], resolution: str) -> None:
    global TEMPRES

    selected, index = value
    print(value)

    if index == 0:
        TEMPRES = 1366,768
        # menu.Menu.resize(height=1080,width=1920)
    elif index == 1:
        TEMPRES = 1280,1024
        # pygame_menu.menu.Menu.resize(height=1024, width=1280)
    else:
        TEMPRES = 800,600
        # pygame_menu.menu.Menu.resize(height=600, width=800)




def resolution():
    pygame.display.set_mode(TEMPRES)
    pygame.display.update()
    print(TEMPRES)





def mainMenu():
    global menu
    menu = pygame_menu.Menu('Welcome', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', game)
    menu.add.button('Settings', settings)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(WIN)

if __name__ == '__main__':
   mainMenu()

'''
ideas for settings:
JSON file to save settings
allow user to change theme for menu in video settings
allow user to change window size from presets <- working on now 
allow user to change audio settings
'''