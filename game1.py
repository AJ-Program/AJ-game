import pygame
import random
import os #operating system
from random import random, randint, seed

WIDTH=800
HEIGHT=600
FPS=30
VEL=10

#define some colors
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#images
#where folders are to setup assets
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"image")

#setup player
class Player(pygame.sprite.Sprite):
    
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(os.path.join(img_folder,"ship.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()#each sprite is a rect
        self.rect.center=(WIDTH-60,HEIGHT-60) #set starting location
        self.x_speed=10

    def update(self):
        self.x_speed=0
        #controls
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed=-10
        if keys[pygame.K_RIGHT]:
            self.x_speed=10
        self.rect.right += self.x_speed

#The monster class code will go here later
class Monster(pygame.sprite.Sprite):
    
    #sprite for the monster
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #initialize the sprite
        self.image= pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect =  self.image.get_rect()
        #self.rect.center= (WIDTH / 2, HEIGHT / 2)
        self.rect.center = (randint(-200,800),  randint(-200,600))
        self.y_speed=5

    def update(self):
        self.rect.x+=5
        self.rect.y+=self.y_speed
        if self.rect.bottom>HEIGHT-1: #下边界
            self.y_speed=-5
        if self.rect.top<1: #上边界
            self.y_speed=5
        if self.rect.left>WIDTH:
            self.rect.right=0


#load graphics
#background
background=pygame.image.load(os.path.join(img_folder,"galaxy.png"))
background_rect=background.get_rect()

#player
ship=pygame.image.load(os.path.join(img_folder,"ship.png"))
ship_rect=ship.get_rect()

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("game name")
clock=pygame.time.Clock()

#group all sprites
all_sprites=pygame.sprite.Group()

#get our player
player=Player()
all_sprites.add(player)

#get a monster
for monster1 in range (1,100):
    monster1=Monster()
    all_sprites.add(monster1)

#game loop
running =True
while running:
    #keep loop running at the speed
    clock.tick(FPS)

    #process inputs(events)
    for event in pygame.event.get():
        #close the window
        if event.type == pygame.QUIT:
            running =False 
    #update
    all_sprites.update()

    #draw /render
    screen.fill(BLACK)
    screen.blit(background,(0,0))
    all_sprites.draw(screen)
    # * after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()