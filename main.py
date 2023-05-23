import pygame
import os
import math
import pygame_menu
import noise
import json


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


SCROLL_THRESH = 200

screen_scroll = 0 
bg_scroll = 0

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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
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
        for i in range(8):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Run/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        # loading  attack images
        temp_list = []
        for i in range(8):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Attack1/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)


        temp_list = []
        for i in range(2):
            img = pygame.image.load(f'Assets/{self.name}/Jump/{i}.png')
            img = pygame.transform.scale (img,(img.get_width(),img.get_height()))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.ismoving = True


        

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

        if self.action < len(self.animation_list):
            animation = self.animation_list[self.action]
            if self.frame_index < len(animation):
                self.image = animation[self.frame_index]

                if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    print(f"Action: {self.action}, Frame Index: {self.frame_index}")
                    self.frame_index += 1

                    if self.frame_index >= len(animation):
                        self.frame_index = 0  # Reset the frame index to loop back to the first image


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

    def Run(self):
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
          

    def Attack1(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def Hurt(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def Death(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def Draw(self):
        WIN.blit(self.image, self.rect)

    def movement(self):

        dx = 0  # when key is pressed, shows the change (delta)
        dy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if not self.is_jumping:
                self.grav = -15
                self.is_jumping = True
        else:
            self.is_jumping = False
        
        if keys[pygame.K_q]:
            self.action = 2

        elif keys[pygame.K_a]:
            dx -= 3
            self.action = 1

        elif keys[pygame.K_d]:
            dx += 3
            self.action = 1

        else:
            self.action = 0


        self.grav += 1
        if self.grav > 10:
            self.grav = 10

        # once the gravity reaches 10, the players doesn't fall at any quicker of a speed

        if self.grav > 10:
            self.grav = 10

        dy += self.grav
        if self.is_jumping and dy > 0:
            self.is_jumping = False

        # updating rect coords 
        self.rect.x += dx
        self.rect.y += dy 

        if self.rect.bottom > SCREENHEIGHT:
            self.rect.bottom = SCREENHEIGHT
            dy = 0
            print(self.rect.bottom)


        if keys[pygame.K_a]:
            rotated_image = pygame.transform.flip(self.image, True, False)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            WIN.blit(rotated_image, rotated_rect)
        
        elif keys[pygame.K_d]:
            non_flipped = pygame.transform.flip(self.image, False, False)
            non_flipped_rect = non_flipped.get_rect(center =  self.rect.center)           
            WIN.blit(non_flipped, non_flipped_rect)

        else:
            self.action = 0
            WIN.blit(self.image, self.rect)
               

def generate_terrain(width, height, octaves=10, persistence=0.5, lacunarity=2, tile_size=16):
    """ Generate a random terrain using Perlin noise algorithm """
    terrain = []
    for i in range(width // tile_size):
        column = []
        for j in range(height // tile_size):
            # Generate base noise
            base_noise_val = noise.pnoise2(i / octaves, 
                                           j / octaves, 
                                           octaves=octaves, 
                                           persistence=persistence, 
                                           lacunarity=lacunarity, 
                                           repeatx=width, 
                                           repeaty=height, 
                                           base=0)
            base_max_height = 10
            base_noise_val = (base_noise_val + 1) * 0.5 * base_max_height
            base_noise_val = int(base_noise_val)
            
            # Generate second layer of noise for variation
            variation_noise_val = noise.pnoise2(i / (octaves * 2), 
                                                j / (octaves * 2), 
                                                octaves=octaves, 
                                                persistence=persistence, 
                                                lacunarity=lacunarity, 
                                                repeatx=width, 
                                                repeaty=height, 
                                                base=0)
            variation_max_height = 2
            variation_noise_val = (variation_noise_val + 1) * 0.5 * variation_max_height
            variation_noise_val = int(variation_noise_val)
            
            # Adjust terrain based on second layer of noise
            if j == base_noise_val:
                if variation_noise_val == 1:
                    # Add a peak
                    tile_rect = pygame.Rect(i * tile_size, (height // tile_size - j - 1) * tile_size, tile_size, tile_size)
                    column.append(tile_rect)
                elif variation_noise_val == 0:
                    # Add a divot
                    column.append(None)
                else:
                    # Use base noise value
                    tile_rect = pygame.Rect(i * tile_size, (height // tile_size - j - 1) * tile_size, tile_size, tile_size)
                    column.append(tile_rect)
            elif j < base_noise_val:
                # Use base noise value
                tile_rect = pygame.Rect(i * tile_size, (height // tile_size - j - 1) * tile_size, tile_size, tile_size)
                column.append(tile_rect)
            else:
                column.append(None)
        terrain.append(column)
    return terrain





def display_fps(surface, clock):
    font = pygame.font.SysFont('Arial', 20)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    fps_pos = fps_text.get_rect()
    fps_pos.topright = surface.get_rect().topright
    surface.blit(fps_text, fps_pos)



class Enemy:
    def __init__(self, x, y, name):
        eimg = pygame.image.load(os.path.join('Assets', 'Enemy', 'Idle', '0.png'))
        self.image = pygame.transform.scale(eimg, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.name = name
        self.direction = 1
        self.rect.y = y
        self.dx = x
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        temp_list = []
        for i in range(4):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)


        temp_list = []
        for i in range(8):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Run/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)


        # loading  attack images
        temp_list = []
        for i in range(4):  # iterates through 8 png for animation
            img = pygame.image.load(f'Assets/{self.name}/Attack1/{i}.png')
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
            temp_list.append(img)  # adds image to image list
        self.animation_list.append(temp_list)

        # hurt images
        temp_list = []
        for i in range(3):  # iterates through 8 png for animation
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

        if self.action < len(self.animation_list):
            animation = self.animation_list[self.action]
            if self.frame_index < len(animation):
                self.image = animation[self.frame_index]

                if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    self.frame_index += 1

                    if self.frame_index >= len(animation):
                        self.frame_index = 0  # Reset the frame index to loop back to the first image


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
        
    def Run(self):
        self.action = 1
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()
        
    def Attack1(self):
        self.action = 2
        self.frame_index = 0 
        self.update_time = pygame.time.get_ticks()


    def Hurt(self):
        # hurt animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def Death(self):
        # hurt animation
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def Reset(self):
        self.alive = True
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def Draw(self):
       
        if self.direction == -1:
            rotated_img = pygame.transform.flip(self.image, True, False)
            WIN.blit(rotated_img, self.rect)
        else:
            WIN.blit(self.image, self.rect)


    def movement(self):
        # set the walking time to 3 seconds (1 second for each direction with a 0.5 second pause)
        walking_time = 3000  # milliseconds
        # set the walking speed to 5 pixels per frame
        walking_speed = 1

        dx = 0 
        
        # calculate the distance to move
        distance = walking_speed * 1

        # determine the current time within the walking time
        current_time = pygame.time.get_ticks() % walking_time

        # move for 1 second to the right
        if current_time < 1000:
            self.direction = 1
            self.action = 1
            # move right
            self.rect.x += distance
            dx += 5

        # pause for 0.5 seconds after moving right
        elif current_time < 1500:
            self.action = 0
            pass  # do nothing

        # move for 1 second to the left
        elif current_time < 2500:
            self.direction = -1
            self.action = 1
            # move left
            self.rect.x -= distance
            
        # pause for 0.5 seconds after moving left
        else:
            self.action = 0
            pass  # do nothing

        # update the player's image and animation
        self.update()


terrain = generate_terrain(SCREENWIDTH, SCREENHEIGHT)

player = Player(200, 150, 'Player')
enemy = Enemy(690, 275, 'Enemy')


def game():
    run = True
    while run:
        BG_Menu.play()
        clock.tick(FPS)
        player.update()
        player.Draw()
    
            
        # blit imgs
        for i in range(0, tile_width):
            WIN.blit(BG_img, (i * BG_width, 0))
        for i in range(0, tile_height):
            WIN.blit(BG_img, (i * BG_height, 0))

        enemy.update()
        enemy.Draw()
        enemy.movement()

        
        display_fps(WIN, clock)
         
        for column in terrain:
            for tile_rect in column:
                if tile_rect is not None:
                    if tile_rect.bottom == SCREENHEIGHT:
                        WIN.blit(grass_image, tile_rect)
                    else:
                        WIN.blit(dirt_image, tile_rect)

        for column in terrain:
            for tile_rect in column:
                if tile_rect is not None and player.rect.colliderect(tile_rect):
                    if player.rect.bottom > tile_rect.top and player.rect.top < tile_rect.top:
                        player.rect.bottom = tile_rect.top
                        player.dx = 0
                    elif player.rect.top < tile_rect.bottom and player.rect.bottom > tile_rect.bottom:
                        player.rect.top = tile_rect.bottom
                        player.dy = 0
                    elif player.rect.right > tile_rect.left and player.rect.left < tile_rect.left:
                        player.rect.right = tile_rect.left
                        player.dy = 0
                    elif player.rect.left < tile_rect.right and player.rect.right > tile_rect.right:
                        player.rect.left = tile_rect.right
                        player.dx = 0
                

        if player.rect.left < 0:
            player.rect.left = 0

        if player.rect.top < 0:
            player.rect.top = 0 

                    

        player.movement()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

        pygame.display.update()


    pygame.quit()


def settings():
    settings = pygame_menu.Menu('Settings', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    settings.add.button('Audio', audio)
    settings.add.button('Keybinds', keybinds) 
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


def keybinds():
    keybind_menu = pygame_menu.Menu('Keybinds', 1000, 406, theme=pygame_menu.themes.THEME_DARK)
    keybind_menu.add.text_input('Move Up:', default='W', onchange=save_keybinds)
    keybind_menu.add.text_input('Move Down:', default='S', onchange=save_keybinds)
    keybind_menu.add.text_input('Move Left:', default='A', onchange=save_keybinds)
    keybind_menu.add.text_input('Move Right:', default='D', onchange=save_keybinds)
    keybind_menu.add.button('Apply', save_keybinds)
    keybind_menu.add.button('Back', settings)
    keybind_menu.mainloop(WIN)

def save_keybinds(value):
    if len(value) >= 3:
        keybinds = {
            'move_up': value[0],
            'move_down': value[1],
            'move_left': value[2],
            'move_right': value[3] if len(value) >= 4 else None
        }
        with open('keybinds.json', 'w') as file:
            json.dump(keybinds, file)




def mainmenu():
    #BG_Menu.play()
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

have enemy damage taken be outputted on y axis and then disappear

to have game end, kill enemy and then slow game time and fade out

have to have a way to store data of players game, score ect

'''
