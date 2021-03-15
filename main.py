# AJ game
import pygame
import random
WIDTH=1000
HEIGHT=500
FPS=30

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("AJ GAME!")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect=self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0
    def update(self):
        self.speedx = 0
        keystate=pygame.key.get_pressed()
# control by keyboard
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect. x+= self.speedx
        # set limit(wall)
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
all_sprites = pygame.sprite.Group()
player=Player()
# can add two players
all_sprites.add(player)
# game loop
running = True
#
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False