import pygame,sys,os,controller,time
from pygame.constants import *
from random import *
from pygame.locals import *

#文件位置
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"image") #图片
snd_folder=os.path.join(game_folder,"sound") #声音
font_folder=os.path.join(game_folder,"font") 

'''
#特殊子弹
class spical_bullets(pygame.sprite.Sprite):
    def __init__(self):#初始化
        super().__init__() #在初始化
        self.image = pygame.image.load(os.path.join(img_folder,"p1_jump.png"))
        self.rect=self.image.get_rect()#在图片周围做切线形成一个矩形（这样图片就可以知道其位置和大小）
        self.speedx,self.speedy = 1,1 #速度一次一个像素点
    def update(self):
        #移动
        self.rect = self.rect.move(self.speedx, self.speedy) #0是横向速度 1是纵向速度，monster移动
        #边界
        if self.rect.left < 0 or self.rect.right > width: #屏幕左上角是（0，0），如果怪物位置左边小于0或者大于宽的长度
            self.speedx = -self.speedx #反相速度，也就是反弹
        if self.rect.right > width and self.rect.right + self.speedx > self.rect.right:#如果接近边缘
            self.speedx = -self.speedx
        if self.rect.top < 0 or self.rect.bottom > height: #上下同理
            self.speedy = -self.speedy
        if self.rect.bottom > height and self.rect.bottom + self.speedy > self.rect.bottom:#同理
            self.speedy = -self.speedy
'''

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #初始化
        self.image = pygame.image.load(os.path.join(img_folder,"ship2.png"))
        self.rect = self.image.get_rect()
        self.rect.center=(player_x,player_y) #玩家初始位置
        self.x=700
        self.y=700

    def update(self):#每次更新
        #玩家速度和控制
        self.x_speed,self.y_speed=0,0

        #定义全局变量
        global player_x,player_y

        keys=pygame.key.get_pressed()

        if self.rect.left < 0:#玩家左边界
            self.rect.left=0
            player_x=0
        elif self.rect.right > width: #右边界
            self.rect.right=width
            player_x=width
        elif keys[pygame.K_LEFT]: #左键
            self.x_speed=-3
            player_x+=self.x_speed
        elif keys[pygame.K_RIGHT]:#右键
            self.x_speed=3
            player_x+=self.x_speed
        self.rect.right += self.x_speed

        if self.rect.top < 0: #同理
            self.rect.top=0
            player_y=0
        elif self.rect.bottom > height:
            self.rect.bottom=height
            player_y=height
        elif keys[pygame.K_UP]:
            self.y_speed=-1.5
            player_y+=self.y_speed
        elif keys[pygame.K_DOWN]:
            self.y_speed=1.5
            player_y+=self.y_speed
        self.rect.bottom += self.y_speed

    def shoot(self):
        bullets = Bullets(self.rect.centerx,self.rect.y)
        all_sprites.add(bullets)
        bullet.add(bullets)

    # def move_controllor(self, movement: tuple = (0, 0)):
    #     self.x += movement[0] * SPEED
    #     self.y += movement[1] * SPEED
        
#BOSS
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #初始化
        self.image = pygame.image.load(os.path.join(img_folder,"Ufo.png"))
        # self.image = pygame.Surface((300,100))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x_speed,self.y_speed = 2,0 #速度
        self.x = 650
        self.rect.center = (self.x,100)#图片中心
    def update(self):
        #移动
        self.rect = self.rect.move(self.x_speed, self.y_speed)
        #边界
        if self.rect.left < 0 or self.rect.right > width: #屏幕左上角是（0，0），如果怪物位置左边小于0或者大于宽的长度
            self.x_speed = -self.x_speed #反相速度，也就是反弹
        #boss移动（变换方向）
        changePosition_L = randint(1,width-1) #随机一个x轴坐标
        if self.x == changePosition_L: #如果运动时x轴相等就变方向
            self.x_speed = -self.x_speed
        if self.rect.right > width and self.rect.right + self.x_speed > self.rect.right:#如果接近边缘
            self.x_speed = -self.x_speed

#子弹
class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"bullet2.png"))
        # self.image = pygame.Surface((10,20))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -5
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite): #Mob
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"p1_jump.png"))
        # self.image = pygame.Surface((50,50))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = randint(400,900)#be sure the bullet comes somewhere from left and right
        self.rect.y = randint(-100,-40)# where the bullet comes from
        self.y_speed = randint(1,2)
        self.x_speed = randint(-1,2)
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.top > height + 10:
            self.rect.x = randint(400,900)
            self.rect.y = randint(-100,-40)
            self.speedy = randint(1,8)

'''
这里以后添加别的类
'''

#获取事件函数
def event_press():
    global running,still
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #记录键盘按下
            if event.key == pygame.K_z or event.key == pygame.K_x:#发射子弹
                player.shoot()
        # elif event.type == KEYUP: #记录键盘按键抬起
            if event.key == pygame.K_ESCAPE:#ESC
                # sys.exit()
                still = True
                pause()

#碰撞判断函数
def hits(): 
    global hit,still
    #check to see if a bullet hit the mob
    hits = pygame.sprite.groupcollide(mobs,bullet,True,True)
    for hit in hits:
       m = Mob()
       all_sprites.add(m)
       mobs.add(m)
    
    #check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player,mobs,False)
    if hits:
        still = True #如果击中就暂停
        Die()

def text_objects1(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def text_objects2(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

# def message_diaplay(text):
#     largeText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),115)
#     TextSurf, TextRect = text_objects2(text, largeText)
#     TextRect.center = ((width/2),(height/2))
#     screen.blit(TextSurf, TextRect)
#     pygame.display.update()
#     time.sleep(2)

def Die():
    largeText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),115)
    TextSurf, TextRect = text_objects2('You   Die', largeText)
    TextRect.center = ((width/2),(height/2))
    screen.blit(TextSurf, TextRect)
 
    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button(" Retry", 500, 450, 120, 50, dark_green, GREEN, game_loop)
        button(" Quit",800, 450, 100, 50, dark_red, RED, quit_game)
        pygame.display.update()
        fclock.tick(15)

def button (msg, x, y, w, h, ic, ac, action=None):
        mouse =pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x,y,w,h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x,y,w,h))
        smallText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"), 40)
        textSurf, textRect = text_objects1(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)))
        screen.blit(textSurf, textRect)

def quit_game():
    pygame.quit()
    quit()

def unpause():
    global still
    still = False

def pause():
    largeText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),115)
    TextSurf, TextRect = text_objects2('Paused', largeText)
    TextRect.center = ((width/2),(height/2))
    screen.blit(TextSurf, TextRect)
 
    while still:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue", 500, 450, 185, 50, dark_green, GREEN, unpause)
        button(" Quit",800, 450, 100, 50, dark_red, RED, quit_game)
        pygame.display.update()
        fclock.tick(15)

def game_intro():
    global still
    still = False
    intro = True
    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # screen.fill(WHITE)
        background=pygame.image.load(os.path.join(img_folder,"background.gif"))
        screen.blit(background,(0,0))

        # largeText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),270)
        # TextSurf, TextRect = text_objects2('Transocks', largeText)
        # TextRect.center = ((width/2),(height/2/2))
        # screen.blit(TextSurf, TextRect)

        button("GO", 500, 450, 100, 50, dark_green, GREEN, game_loop)
        button(" Quit",800, 450, 100, 50, dark_red, RED, quit_game)
        pygame.display.update()
        fclock.tick(15)

def game_loop():
    #背景
    background=pygame.image.load(os.path.join(img_folder,"backgroundPic.jpg"))

    running = True
    while running: #循环，一直获取用户的命令并执行
        # for event in pygame.event.get():
        event_press()
            #窗口
            # if event.type == pygame.VIDEORESIZE: #让边界随窗口大小而改变
            #     size = width, height = event.size[0], event.size[1]
            #     screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        # p1.update()
        # player.move_controllor(p1.get_axis())

        if pygame.display.get_active() and not still: #判断程序是否最小化，最小化后暂停
            all_sprites.update() #更新精灵类

        #填充和显示
        screen.fill(WHITE)#每次移动填充的颜色
        screen.blit(background,(0,0))#显示背景

        all_sprites.draw(screen) #显示导入到精灵类的屏幕
        
        pygame.display.update() #刷新屏幕

        fclock.tick(fps)#控制刷新速度（每秒钟刷新fps次）

        hits()

BLACK = (0,0,0)#设置颜色
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
dark_red = (200,0,0)
dark_green = (0,200,0)
fps = 300#每秒钟帧率
fclock = pygame.time.Clock()#Clock对象，用于控制时间

#图标
icon = pygame.image.load(os.path.join(img_folder,"ship2.png"))
pygame.display.set_icon(icon)

#玩家坐标
player_x=700
player_y=700

#Boss坐标
Boss_x=650
Boss_y=100

#玩家手柄
SPEED=10
# p1 = controller.Controller(0)

#是否移动
still = False #用来判断暂停

size = width, height = 1400, 800 #屏幕大小为当前电脑屏幕大小
screen = pygame.display.set_mode(size,RESIZABLE) #应用屏幕大小，（可伸缩屏幕）
pygame.display.set_caption("Transocks") #游戏名

#创建一个精灵空组
all_sprites=pygame.sprite.Group() 
mobs = pygame.sprite.Group()
bullet = pygame.sprite.Group()

#获取类
player=Player()
boss=Boss()
#spical_bullet=spical_bullets()

for i in range(30): #敌人子弹数
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#放入精灵类
all_sprites.add(player) #添加进精灵组
all_sprites.add(boss) 
#all_sprites.add(spical_bullet)

# Jason Xiao, Alex Li
# Transocks
# March 7 2021

pygame.init()

game_intro()

game_loop()