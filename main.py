import pygame
import os
import math
import pygame_menu
import noise


# TO DO LIST = NEED TO HAVE MENU RESOLUTIONS WORKING, NEED TO HAVE TERRAIN WORKING.


pygame.init()
pygame.display.init()
pygame.mixer.init()

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
BG_Menu = pygame.mixer.Sound(os.path.join('Assets', 'Pyre Original Soundtrack - Downside Ballad.mp3'))
BG_Menu.set_volume(1)

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
        self.angle = 0
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

        temp_list = []
        for i in range(2):
            img = pygame.image.load(f'Assets/{self.name}/Jump/{i}.png')
            img = pygame.transform.scale (img,(img.get_width(),img.get_height()))
            temp_list.append(img)
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

    def Jump(self):

        self.action = 1
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

    def camera(player_pos):
    
     # Get the width and height of the game window
        width = pygame.display.get_surface().get_width()
        win_height = pygame.display.get_surface().get_height()

        # Calculate the center of the game window
        center_x = win_width // 2
        center_y = win_height // 2

        # Get the position of the player
        player_x, player_y = player_pos

        # Calculate the offset needed to center the player
        offset_x = center_x - player_x
        offset_y = center_y - player_y

        # Move the game window by the offset
        WIN_OFFSET[0] = offset_x
        WIN_OFFSET[1] = offset_y

        camera((self.rect.x, self.rect.y))

        

    def movement(self):

        dx = 0  # when key is pressed, shows the change (delta)
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.Jump()
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



        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        WIN.blit(rotated_image, rotated_rect)

class Terrain:
    def __init__(self):
        # Initialize terrain data
        self.terrain_data = []

        # Generate terrain data
        self.generate_terrain_data()

    def generate_terrain_data(self):
        # Generate terrain data using Perlin noise
        for x in range(SCREENWIDTH // TILE_SIZE - 1, -1, -1):
            # Determine height of terrain using Perlin noise
            terrain_height = int((1 + noise.pnoise1(x / 30, repeat=9999)) * 3) + 3

            # Generate column of terrain data
            column = []
            for y in range(terrain_height):
                if y == 0:
                    # Use grass for top layer
                    tile_image = grass_image
                else:
                    # Use dirt for other layers
                    tile_image = dirt_image

                tile_rect = pygame.Rect(x * TILE_SIZE,
                                        (SCREENHEIGHT - (terrain_height * TILE_SIZE)) + (y * TILE_SIZE),
                                        TILE_SIZE, TILE_SIZE)
                column.append({'image': tile_image, 'rect': tile_rect})

            self.terrain_data.append(column)

    def draw(self, surface):
        # Draw terrain tiles to the screen
        for column in self.terrain_data:
            for tile in column:
                surface.blit(tile['image'], tile['rect'])

    def get_tile_at_position(self, x, y):
        # Get the terrain tile at a given position
        column_index = x // TILE_SIZE
        row_index = (y - (SCREENHEIGHT - (len(self.terrain_data[column_index]) * TILE_SIZE))) // TILE_SIZE

        if column_index < 0 or column_index >= len(self.terrain_data):
            return None

        if row_index < 0 or row_index >= len(self.terrain_data[column_index]):
            return None

        return self.terrain_data[column_index][row_index]['rect']


player = Player(200, 150, 'Player')
terrain = Terrain()



def game():
    run = True
    while run:
        # BG_Menu.play()
        clock.tick(FPS)

        player.update()
        player.Draw()
        camera(player.get_position())

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






# menu shit


def settings():
    settings = pygame_menu.Menu('Settings', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    settings.add.button('Audio', audio)
    settings.add.button('Back', mainmenu)
    settings.mainloop(WIN)


def audio():
    audio = pygame_menu.Menu('Audio', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    volRange = audio.add.range_slider("Volume", 0, (0, 100), 10, set_volume)
    audio.add.button('Apply', lambda: set_volume(volRange.get_value()))
    audio.add.button('Back', settings)
    audio.mainloop(WIN)


def set_volume(value):
    BG_Menu.set_volume(value//100)
    




# window won't resize if the res chosen first is in the list without scrolling breaks code for some reason?


def mainmenu():
    BG_Menu.play()
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
