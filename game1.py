# Jason Xiao, Alex Li
# Transocks
# March 7 2021

import pygame,sys,os

from pygame.constants import KEYUP, K_DOWN, K_LEFT, K_RIGHT, K_UP, RESIZABLE

#文件位置
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"image") #图片
snd_folder=os.path.join(game_folder,"sound") #声音

BLACK = (0,0,0)#设置一种颜色

fps = 300#每秒钟帧率
fclock = pygame.time.Clock()#Clock对象，用于控制时间

pygame.init() #初始化------这里开始是主程序

size = width, height = 1400, 800 #屏幕大小为当前电脑屏幕大小
screen = pygame.display.set_mode(size,RESIZABLE) #应用屏幕大小，（可伸缩屏幕）
pygame.display.set_caption("Transocks") #游戏名

#背景
background=pygame.image.load(os.path.join(img_folder,"galaxy.png")).convert()
background_rect=background.get_rect()

#怪物（以后会改）
monster = pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()
monster_rect=monster.get_rect()#在图片周围做切线形成一个矩形（这样图片就可以知道其位置和大小）
monster_speed = [1,1] #速度一次一个像素点

#玩家（以后会改）
player = pygame.image.load(os.path.join(img_folder,"ship.png")).convert()
player_rect = player.get_rect()
player_x,player_y=700,700
player_movex, player_movey = 0,0


#图标
icon = pygame.image.load(os.path.join(img_folder,"ship.png"))
pygame.display.set_icon(icon)

#是否移动
still = False

while True: #循环，一直获取用户的命令并执行
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: #记录键盘按下
            #键盘控制
            if event.key == K_LEFT:
                player_movex=-1
            elif event.key == K_RIGHT:
                player_movex=1
            elif event.key == K_UP:
                player_movey=-1
            elif event.key == K_DOWN:
                player_movey=1
        elif event.type == KEYUP: #记录键盘按键抬起
            if event.key == K_LEFT:
                player_movex=0
            if event.key == K_RIGHT:
                player_movex=0
            if event.key == K_UP:
                player_movey=0
            if event.key == K_DOWN:
                player_movey=0
            elif event.key == pygame.K_ESCAPE:#ESC退出游戏
                    sys.exit()
    
        elif event.type == pygame.VIDEORESIZE: #让边界随窗口大小而改变
            size = width, height = event.size[0], event.size[1]
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN: #如果鼠标按下那么停止移动
            if event.button == 1:
                still = True
        elif event.type == pygame.MOUSEBUTTONUP: #如果鼠标释放那么到达鼠标的位置并继续运动
            still = False
            if event.button == 1:
                monster_rect = monster_rect.move(event.pos[0] - monster_rect.left, event.pos[1] - monster_rect.top)
        elif event.type == pygame.MOUSEMOTION: #鼠标移动图片跟随鼠标
            if event.buttons[0] == 1:
                monster_rect = monster_rect.move(event.pos[0] - monster_rect.left, event.pos[1] - monster_rect.top)
    

    if pygame.display.get_active() and not still: #判断程序是否最小化，最小化后暂停
        monster_rect = monster_rect.move(monster_speed[0], monster_speed[1]) #0是横向速度 1是纵向速度

    #怪物边界
    if monster_rect.left < 0 or monster_rect.right > width: #屏幕左上角是（0，0），如果怪物位置左边小于0或者大于宽的长度
        monster_speed[0] = -monster_speed[0] #反相速度，也就是反弹
        if monster_rect.right > width and monster_rect.right + monster_speed[0] > monster_rect.right:#如果接近边缘
            monster_speed[0] = -monster_speed[0]
    if monster_rect.top < 0 or monster_rect.bottom > height: #上下同理
        monster_speed[1] = -monster_speed[1]
        if monster_rect.bottom > height and monster_rect.bottom + monster_speed[1] > monster_rect.bottom:#同理
            monster_speed[1] = -monster_speed[1]

    #玩家移动
    player_x+=player_movex
    player_y+=player_movey

    # 玩家边界(没做完)
    if player_x < 0: 
        player_x=0
    if player_x > width-40:
        player_x = width-40#减去图片本身大小
    if player_y < 0:
        player_y=0
    if player_y > height-40: 
        player_y = height-40 #减去图片本身大小

    screen.fill(BLACK)#每次怪物移动填充的颜色
    screen.blit(background,background_rect)#显示背景
    screen.blit(monster,monster_rect)#显示怪物
    screen.blit(player,(player_x,player_y))#显示玩家
    
    pygame.display.update() #刷新屏幕

    fclock.tick(fps)#控制刷新速度（每秒钟刷新fps次）