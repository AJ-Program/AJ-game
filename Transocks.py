import pygame,os,controller,sys
from pygame.constants import *
from random import *
from pygame.locals import *

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
        self.image = pygame.image.load(os.path.join(img_folder,"player.png"))
        self.rect = self.image.get_rect()
        self.radius = 14
        #pygame.draw.circle(self.image,RED,self.rect.center, self.radius)
        self.x=Player_x
        self.y=Player_y
        self.rect.center=(self.x,self.y) #玩家初始位置
        self.shield = 239

    def update(self):#每次更新
        #玩家速度和控制
        self.x_speed,self.y_speed=0,0

        keys=pygame.key.get_pressed()

        if self.rect.left < 0:#玩家左边界
            self.rect.left=0
            self.x=0
        elif self.rect.right > width: #右边界
            self.rect.right=width
            self.x=width
        elif keys[pygame.K_LEFT]: #左键
            self.x_speed=-3
            self.x+=self.x_speed
        elif keys[pygame.K_RIGHT]:#右键
            self.x_speed=3
            self.x+=self.x_speed
        self.rect.right += self.x_speed

        if self.rect.top < 0: #同理
            self.rect.top=0
            self.y=0
        elif self.rect.bottom > height:
            self.rect.bottom=height
            self.y=height
        elif keys[pygame.K_UP]:
            self.y_speed=-3
            self.y+=self.y_speed
        elif keys[pygame.K_DOWN]:
            self.y_speed=3
            self.y+=self.y_speed
        self.rect.bottom += self.y_speed

    def shoot(self):
        bullets = Bullets(self.rect.centerx,self.rect.y)
        all_sprites.add(bullets)
        bullet.add(bullets)

    def reset(self):    # 添加重生的方法
        global still,times_retry
        player.shield=239
        self.rect.left, self.rect.bottom = Player_x, Player_y
        still = False
        times_retry+=1
        
    # def move_controllor(self, movement: tuple = (0, 0)):
    #     self.x += movement[0] * SPEED
    #     self.y += movement[1] * SPEED

'''
#BOSS
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #初始化
        self.image = pygame.image.load(os.path.join(img_folder,"boss.png"))
        # self.image = pygame.Surface((300,100))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        #initial shield of boss
        # self.shield=100
        self.x_speed,self.y_speed = 2,0 #速度
        self.x = 650
        self.rect.center = (self.x,100)#图片中心

    # def update(self):
    #     #移动
    #     self.rect = self.rect.move(self.x_speed, self.y_speed)
    #     #边界
    #     if self.rect.left < 0 or self.rect.right > width: #屏幕左上角是（0，0），如果怪物位置左边小于0或者大于宽的长度
    #         self.x_speed = -self.x_speed #反相速度，也就是反弹
    #     #boss移动（变换方向）
    #     changePosition_L = randint(1,width-1) #随机一个x轴坐标
    #     if self.x == changePosition_L: #如果运动时x轴相等就变方向
    #         self.x_speed = -self.x_speed
    #     if self.rect.right > width and self.rect.right + self.x_speed > self.rect.right:#如果接近边缘
    #         self.x_speed = -self.x_speed

'''

#子弹
class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"bullet2.png"))
        # self.image = pygame.Surface((10,20))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #radius of bullet, so that subtract with boss' sheld 
        # self.radius = int(self.rect.width)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

#Mob
class Mob(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        mob = []
        mob.append(pygame.image.load(os.path.join(img_folder,"mob1.png")))
        mob.append(pygame.image.load(os.path.join(img_folder,"mob2.1.png")))
        self.image = mob[randint(0,1)]
        # self.image = pygame.Surface((50,50))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #pygame.draw.circle(self.image,RED,self.rect.center, self.radius)
        self.rect.x = randint(400,900)#be sure the bullet comes somewhere from left and right
        self.rect.y = randint(-100,-40)# where the bullet comes from
        self.y_speed = randint(4,5)
        self.x_speed = randint(-9,9)
    def update(self):
        if self.rect.left < 0 or self.rect.right > width:
            self.x_speed = -self.x_speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.top > height + 10:
            self.rect.x = randint(400,900)
            self.rect.y = randint(-100,-40)
            self.speedy = randint(1,8)

#获取事件函数
def event_press():
    global running,still
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #记录键盘按下
            if event.key == pygame.K_z:#发射子弹
                player.shoot()
        # elif event.type == KEYUP: #记录键盘按键抬起
            if event.key == pygame.K_ESCAPE:#ESC
                # sys.exit()
                still = True
                pause()
    
#碰撞判断函数
def hits(): 
    global hit,still,player_live,score
    #check to see if a bullet hit the mob
    hits = pygame.sprite.groupcollide(mobs,bullet,True,True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score+=1
        if Die:
            score_count.clear()
            score_count.append(score)
            # print(score_count)
            

    hits = pygame.sprite.spritecollide(player,mobs,True ,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius*2
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

        if player.shield<=0:
            score = 0
            Die()
    
    '''set a function for boss(when bullet hits him)
    hits = pygame.sprite.spritecollide(bullet,boss,True ,pygame.sprite.collide_circle)
    for hit in hits:
        b.shield -= hit.radius
        m = Boss()
    '''

def text_objects1(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def text_objects2(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def text_objects3(text, font):
    textSurface = font.render(text, True, GREEN)
    return textSurface, textSurface.get_rect()

#死亡界面
def Die():
    pygame.mixer.music.pause()
    largeText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),115)
    TextSurf, TextRect = text_objects3('Game   Over!', largeText)
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

#按钮
def button (msg, x, y, w, h, ic, ac, action=None):
    click = pygame.mouse.get_pressed()
    mouse =pygame.mouse.get_pos()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == True and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    smallText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"), 40)
    textSurf, textRect = text_objects1(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def score_text():
    global score
    score_font = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),40)
    score_surface = score_font.render("Score  %s" % str(score), True, BLUE)
    screen.blit(score_surface,(30,20))

def timer_text():
    global dt,timer

    timer -= dt
    if timer <= 0:
        timer = 120
        Die()

    txt = font.render(str(round(timer, 2)), True, BLUE)
    screen.blit(txt, (20, 70))
    dt = fclock.tick(300) / 400  # / 1000 to convert to seconds.

def txt_create(name): 
    global names
    result_score = []
    result_retry = []
    result_time = []

    #获得数值
    if player.shield<=0:
        if len(score_count) == 0: #如果数组为空
            result_score.append("Score:"+"0")
        else:
            result_score.append(": "+"Score:"+str(max(score_count)))
        result_retry.append("Retry:"+str(times_retry))
        result_time.append("Time:"+format(120-timer, '.2f'))
    total = [result_score,result_retry,result_time]

    #创建文件
    desktop_path = sys.argv[0] # 新创建的txt文件的存放路径    
    full_path = desktop_path + "_" + name + '.txt'   #也可以创建一个.doc的word文档    
    file = open(full_path, '+a')    # w 的含义为可进行读写

    #写入文件
    # file.write('score\tretry\ttime\n')
    for row in total:
        rowtxt = '{}'.format(row[0])
        file.write(rowtxt)
        file.write(' ')
    file.write('\n')
    file.close() 

def rank_list():#排行榜
    # file_path = sys.path[0]+'/Transocks.py_log1.txt'
    # print(score,'\t',times_retry,'\t',format(120-timer, '.2f'),"s",sep='')
    
    txt_create("log1")
    read_rewrite()

def read_rewrite():
    #读取文件
    read_data = []

    with open(sys.path[0]+'/Transocks.py_log1.txt', 'r') as f:
        for line in f:#遍历每一行
            line = line.replace("Score", "")
            line = line.replace("Retry", "")
            line = line.replace("Time", "")
            line = line.replace(":", "")
            line
            line = line.split()#将每一行的数字分开放在列表中
            read_data.append(line)
        for i in range(0,len(read_data)):
            for j in range(3):
                read_data[i].append(float(read_data[i][j]))
            del(read_data[i][0:3])
    print(sorted(read_data,key=(lambda x:[x[0],x[2],x[1]])))
    f.close()

    #重写部分
    # file=open(sys.path[0]+'/Transocks.py_log1.txt', 'w')
    # for i in read_data:
    #     print(i)
    #     #重写覆盖
    #     file.write(i)
    #     file.write('\n')
    # file.close()

def quit_game():

    rank_list()

    pygame.quit()
    quit()

def quit_game1():
    pygame.quit()
    quit()

#未暂停
def unpause():
    global still
    still = False
    pygame.mixer.music.unpause()

#暂停
def pause():
    pygame.mixer.music.pause()
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

def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,239,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,RED,outline_rect,2)

#游戏开始界面
def game_intro():
    global still,names
    still = False
    intro = True
    count = 0
    background_intro = []

    #输入框变量
    input_box = pygame.Rect(150,350,140,31)
    color_inactive = GREEN
    color_active = dark_green
    color = color_inactive
    text = ''
    names = []
    active = False

    #动态背景
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background1.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background2.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background3.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background4.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background5.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background6.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background7.png")))
    for i in range(1,11):
        background_intro.append(pygame.image.load(os.path.join(img_folder,"background8.png")))

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text) #输出文字
                        # names.append(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        #背景
        background_intro1 = background_intro[count]

        screen.blit(background_intro1,(0,0))

        count+=1

        if count > 79:
            count = 0

        # largeText = pygame.font.Font(os.path.join(font_folder,"arcadeclassic.ttf"),270)
        # TextSurf, TextRect = text_objects2('Transocks', largeText)
        # TextRect.center = ((width/2),(height/2/2))
        # screen.blit(TextSurf, TextRect)

        #input box
        text_surface = font.render(text, True, color)
        width = max(200, text_surface.get_width()+10)
        input_box.w = width
        screen.blit(text_surface,(input_box.x+5,input_box.y-8))
        pygame.draw.rect(screen,color,input_box,5)
        
        #按钮
        button("GO", 500, 450, 100, 50, dark_green, GREEN, game_loop)
        button(" Quit",800, 450, 100, 50, dark_red, RED, quit_game1)
        pygame.display.update()
        fclock.tick(15)

def game_loop():
    global timer
    
    player.reset()

    #reset timer
    if times_retry>0:
        timer = 120  # Reset it to 10 or do something else.
        pygame.mixer.music.unpause()
    elif times_retry==0:
        #bgm
        pygame.mixer.music.play(-1) 

    #背景
    background=pygame.image.load(os.path.join(img_folder,"backgroundPic.jpg"))  
    
    running = True
    while running: #循环，一直获取用户的命令并执行
        event_press()

        if pygame.display.get_active() and not still: #判断程序是否最小化，最小化后暂停
            all_sprites.update() #更新精灵类

        #填充和显示
        screen.fill(WHITE)#每次移动填充的颜色
        screen.blit(background,(0,0))#显示背景
        score_text()
        timer_text()
        # rank_list()

        #draw
        draw_shield_bar(screen,1050,750,player.shield)
        #another bar for boss' health
        # draw_shield_bar(screen,1150,80,boss.shield)

        all_sprites.draw(screen) #显示导入到精灵类的屏幕
        
        pygame.display.update() #刷新屏幕

        fclock.tick(fps)#控制刷新速度（每秒钟刷新fps次）

        hits()

#文件位置
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"image") #图片
snd_folder=os.path.join(game_folder,"sound") #声音
font_folder=os.path.join(game_folder,"font") 

pygame.init()

#timer设置
font = pygame.font.Font(os.path.join(font_folder,"LockClock.ttf"), 35)
timer = 120  # Decrease this to count down.
dt = 0  # Delta time (time since last tick).

BLACK = (0,0,0)#设置颜色
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
dark_red = (200,0,0)
dark_green = (0,200,0)
BLUE = (0,0,255)
fps = 300#每秒钟帧率
fclock = pygame.time.Clock()#Clock对象，用于控制时间

#图标
icon = pygame.image.load(os.path.join(img_folder,"player.png"))
pygame.display.set_icon(icon)

#玩家坐标
Player_x=700
Player_y=700

#Boss坐标
Boss_x=650
Boss_y=100

score=0#分数
score_count = []

#玩家手柄


#是否暂停
still = False #用来判断暂停

#重试次数
times_retry = -1

#bgm
pygame.mixer.music.load(os.path.join(snd_folder,"bgm.mp3"))

size = width, height = 1400, 800 #屏幕大小为当前电脑屏幕大小
screen = pygame.display.set_mode(size)#,RESIZABLE) #应用屏幕大小，（可伸缩屏幕）
pygame.display.set_caption("Transocks") #游戏名

#创建一个精灵空组
all_sprites=pygame.sprite.Group() 
p=pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullet = pygame.sprite.Group()
boss = pygame.sprite.Group()

#获取类
player=Player()
# b=Boss()
#spical_bullet=spical_bullets()

for i in range(30): #小怪数
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# for i in range(3): #子弹数
#     m = Bullets(player.rect.centerx,player.rect.y)
#     all_sprites.add(m)
#     bullet.add(m)

#放入精灵类
all_sprites.add(player) #添加进精灵组
# all_sprites.add(b) 
#all_sprites.add(spical_bullet)

# Jason Xiao, Alex Li
# Transocks
# March 7 2021

game_intro()

game_loop()