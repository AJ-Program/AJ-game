# Jason Xiao, Alex Li
# Transocks
# March 7 2021

import pygame,sys,os,math
from pygame.constants import *
from random import *

#文件位置
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"image") #图片
snd_folder=os.path.join(game_folder,"sound") #声音

#怪物（以后会改）特殊子弹
class spical_bullets(pygame.sprite.Sprite):
    def __init__(self):#初始化
        pygame.sprite.Sprite.__init__(self)
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

#玩家
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"ship.png"))
        self.rect = self.image.get_rect()
        self.rect.center=(player_x,player_y) #玩家初始位置

    def update(self):#每次更新
        #玩家速度和控制
        self.x_speed=0
        self.y_speed=0

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
            self.x_speed=-1
            player_x+=self.x_speed
        elif keys[pygame.K_RIGHT]:#右键
            self.x_speed=1
            player_x+=self.x_speed
        self.rect.right += self.x_speed
        # print(self.x) #获得x轴坐标

        if self.rect.top < 0: #同理
            self.rect.top=0
            player_y=0
        elif self.rect.bottom > height:
            self.rect.bottom=height
            player_y=height
        elif keys[pygame.K_UP]:
            self.y_speed=-1
            player_y+=self.y_speed
        elif keys[pygame.K_DOWN]:
            self.y_speed=1
            player_y+=self.y_speed
        self.rect.bottom += self.y_speed

#BOSS
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"Ufo.png"))
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

# #子弹与怪物距离函数
# def distance(bx,by,Bx,By):#子弹xy轴坐标和Boss xy轴坐标，计算子弹和敌人的距离
#     distance_x = bx - Bx
#     distance_y = by - By
#     return math.sqrt(distance_x*distance_x + distance_y*distance_y) #开根号，勾股定理
# print(distance(1,1,4,5))

#子弹
bullets_save = [] #保存子弹，并且当子弹移除窗口时删除
class Bullets():
    def __init__(self):
        self.image = pygame.image.load(os.path.join(img_folder,"bullets.gif"))
        self.x = player_x-70
        self.y = player_y-120
        self.speed=5
    # def hit(self):
    #     for i in range (0,10):
    #         if (distance(self.x, self.y, i.x, i.y)<30):
    #             bullets_save.remove(self)

#显示子弹函数
def show_bullet():
    for b in bullets_save:
        screen.blit(b.image,(b.x,b.y))
        b.y -= b.speed
        if b.y < 0:
            bullets_save.remove(b)

#获取事件函数
def event_press():
    if event.type == pygame.QUIT:
        sys.exit()
    # elif event.type == pygame.KEYDOWN: #记录键盘按下
    elif event.type == KEYUP: #记录键盘按键抬起
        if event.key == pygame.K_ESCAPE:#ESC退出游戏
            sys.exit()
        if event.key == pygame.K_z or event.key == pygame.K_x:#空格发射子弹
            bullets_save.append(Bullets()) #创建子弹并加入数组

    # # 鼠标可以拖动图片 (没做完)********
    # elif event.type == pygame.MOUSEBUTTONDOWN: #如果鼠标按下那么停止移动
    #     if event.button == 1:
    #         still = True
    # elif event.type == pygame.MOUSEBUTTONUP: #如果鼠标释放那么到达鼠标的位置并继续运动
    #     still = False
    #     if event.button == 1:
    #         player_rect = player_rect.move(event.pos[0] - player_rect.left, event.pos[1] - player_rect.top)
    # elif event.type == pygame.MOUSEMOTION: #鼠标移动图片跟随鼠标
    #     if event.buttons[0] == 1:
    #         player_rect = player_rect.move(event.pos[0] - player_rect.left, event.pos[1] - player_rect.top)


'''
这里以后添加别的类
'''

BLACK = (0,0,0)#设置一种颜色

fps = 300#每秒钟帧率
fclock = pygame.time.Clock()#Clock对象，用于控制时间

#图标
icon = pygame.image.load(os.path.join(img_folder,"ship.png"))
pygame.display.set_icon(icon)

#背景
background=pygame.image.load(os.path.join(img_folder,"background.gif"))
background_rect=background.get_rect()

#玩家坐标
player_x=700
player_y=700

#是否移动
still = False #用来判断最小化时暂停

size = width, height = 1400, 800 #屏幕大小为当前电脑屏幕大小
screen = pygame.display.set_mode(size,RESIZABLE) #应用屏幕大小，（可伸缩屏幕）
pygame.display.set_caption("Transocks") #游戏名

#组一起
all_sprites=pygame.sprite.Group()

#获取类
player=Player()
boss=Boss()
spical_bullet=spical_bullets()

#放入精灵类
all_sprites.add(player)
all_sprites.add(boss)
all_sprites.add(spical_bullet)

while True: #循环，一直获取用户的命令并执行
    for event in pygame.event.get():
        event_press()
        #窗口
        if event.type == pygame.VIDEORESIZE: #让边界随窗口大小而改变
            size = width, height = event.size[0], event.size[1]
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    if pygame.display.get_active() and not still: #判断程序是否最小化，最小化后暂停
        all_sprites.update() #更新精灵类

    #填充和显示
    screen.fill(BLACK)#每次移动填充的颜色
    screen.blit(background,(0,0))#显示背景
    show_bullet()

    all_sprites.draw(screen) #显示导入到精灵类的屏幕
    
    pygame.display.update() #刷新屏幕

    fclock.tick(fps)#控制刷新速度（每秒钟刷新fps次）