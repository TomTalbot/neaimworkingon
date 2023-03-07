

import pygame
import os
import math
import pygame_menu
import noise


# TO DO LIST = NEED TO HAVE MENU RESOLUTIONS WORKING, NEED TO HAVE TERRAIN WORKING.


pygame.init()
pygame.display.init()
pygame.mixer.init()

global TEMPRES

clock = pygame.time.Clock()
FPS = 60

SCREENWIDTH, SCREENHEIGHT = 1000, 406

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)


TILE_SIZE = 16



WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Óendanlegt')




# Audio loading
# BG_Menu = pygame.mixer.Sound(os.path.join('Assets', 'Whatisthatmelody.mp3'))
# BG_Menu.set_volume(1)

# draw stuff
BG_img = pygame.image.load(os.path.join('Assets', 'BG.png'))
BG_width = BG_img.get_width()
BG_height = BG_img.get_height()

dirt_image = pygame.image.load(os.path.join('Assets', 'dirt.png'))
grass_image = pygame.image.load(os.path.join('Assets', 'grass.png'))

# math.ceil rounds number up, tile width calculates the number of tiles needed to be blitted to fill screen
tile_width = math.ceil(SCREENWIDTH / BG_width)
tile_height = math.ceil(SCREENHEIGHT / BG_height)


class Player:
    def __init__(self, x, y, name):
        pimg = pygame.image.load(os.path.join('Assets', 'Player', 'Idle', '0.png'))
        self.image = pygame.transform.scale(pimg, (350, 350))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.name = name
        self.rect.y = y
        self.dx = x
        self.dy = y
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.grav = 0
        self.update_time = pygame.time.get_ticks()

        temp_list = []
        for i in range(8):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        # loading  attack images
        temp_list = []
        for i in range(6):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Attack1/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        # hurt images
        temp_list = []
        for i in range(4):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        temp_list = []
        for i in range(6):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        # adds temp list to master list, creates list of lists, all animations passed through temp list will be added to
        # the master list
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        animation_cooldown = 100  # milliseconds
        # handles animation
        # updates image
        self.image = self.animation_list[self.action][self.frame_index]
        # if the current time and update time are greater than 100ms then change to the next image in animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # if animation is done, loop to first image
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.Idle()

    def Idle(self):

        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def Hurt(self):
        # hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        def Death(self):
            # hurt animation
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def Reset(self):
        self.alive = True
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def Draw(self):
        WIN.blit(self.image, self.rect)

    def movement(self):

        dx = 0  # when key is pressed, shows the change (delta)
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.grav = -15  # neg value increase y coord
        if keys[pygame.K_a]:
            dx -= 5
        if keys[pygame.K_d]:
            dx += 5

        self.grav += 1

        # once the gravity reaches 10, the players doesn't fall at any quicker of a speed

        if self.grav > 10:
            self.grav = 10

        dy += self.grav

        # updating coords
        self.rect.x += dx
        self.rect.y += dy


        WIN.blit(self.image, self.rect)


class Terrain:
    def __init__(self):
        # Initialize terrain data
        self.terrain_data = []

        # Generate terrain data
        self.generate_terrain_data()

    def generate_terrain_data(self):
        # Generate terrain data using Perlin noise
        for x in range(SCREENWIDTH // TILE_SIZE):
            # Determine height of terrain using Perlin noise
            terrain_height = int((1 + noise.pnoise1(x / 30, repeat=9999)) * 3) + 3

            # Generate column of terrain data
            column = []
            for y in range(terrain_height):
                if y == terrain_height - 1:
                    # Use grass for top layer
                    tile_image = grass_image
                else:
                    # Use dirt for other layers
                    tile_image = dirt_image

                column.append({'image': tile_image, 'rect': pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)})

            self.terrain_data.append(column)

    def draw(self, surface):
        # Draw terrain tiles to the screen
        for column in self.terrain_data:
            for tile in column:
                surface.blit(tile['image'], tile['rect'])

    def get_tile_at_position(self, x, y):
        # Get the terrain tile at a given position
        column_index = x // TILE_SIZE
        row_index = y // TILE_SIZE

        if column_index < 0 or column_index >= len(self.terrain_data):
            return None

        if row_index < 0 or row_index >= len(self.terrain_data[column_index]):
            return None

        return self.terrain_data[column_index][row_index]['rect']


player = Player(100, 100, 'Player')
terrain = Terrain()



def game():
    run = True
    while run:
        # BG_Menu.play()
        clock.tick(FPS)

        player.update()
        player.Draw()

        # blit imgs
        for i in range(0, tile_width):
            WIN.blit(BG_img, (i * BG_width, 0))
        for i in range(0, tile_height):
            WIN.blit(BG_img, (i * BG_height, 0))

        player.movement()

        terrain.draw(WIN)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

        pygame.display.update()


    pygame.quit()



# menu shit


'''
BUTTON_STYLE = {
    "hover_color": BLUE,
    "clicked_color": GREEN,
    "clicked_font_color": BLACK,
    "hover_font_color": ORANGE,
}
'''



# menu shit


def settings():
    settings = pygame_menu.Menu('Settings', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    settings.add.button('Audio', audio)
    settings.add.button('Video', video)
    settings.add.button('Back', mainmenu)
    settings.mainloop(WIN)


def audio():
    global volRange
    audio = pygame_menu.Menu('Audio', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    volRange = audio.add.range_slider("Volume", 0, (0, 100), 10, set_volume)
    audio.add.button('Apply', set_volume)
    audio.add.button('Back', settings)
    audio.mainloop(WIN)


def set_volume():
    a = volRange.get_value()
    print(a)


def video():
    video = pygame_menu.Menu('Video', 1000, 406, theme=pygame_menu.themes.THEME_DARK)

    # all example resolutions
    def set_resolution(value, resolution):
        global screen_width, screen_height
        screen_width, screen_height = resolution
        pygame.display.set_mode((screen_width, screen_height))



    resolutions = [('800 x 600', (800, 600)), ('1024 x 768', (1024, 768)), ('1280 x 720', (1280, 720)), ('1920 x 1080', (1920, 1080))]
    resolution_selector = video.add.selector('Resolution: ', resolutions, onchange=set_resolution)
    video.add.button('Back', settings)
    video.mainloop(WIN)



# window won't resize if the res chosen first is in the list without scrolling breaks code for some reason?


def mainmenu():
    menu = pygame_menu.Menu('Welcome', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', game)
    menu.add.button('Settings', settings)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(WIN)


if __name__ == '__main__':
    mainmenu()



'''
ideas for settings:
JSON file to save settings
allow user to change theme for menu in video settings
allow user to change window size from presets <- potentially scrapped?
allow user to change audio settings <- need to have the main 

for enemy generation -> grab all x and y pos of all tiles in terrain append them to a list then have enemy spawn if the
random coords assigned are not in the list.


have enemy damage taken be outputted on y axis and then disappear

to have game end, kill enemy and then slow game time and fade out

have to have a way to store data of players game, score ect

'''
if __name__ == 'main':
    mainmenu()
