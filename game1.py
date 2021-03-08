# Jason Xiao, Alex Li
# 游戏名
# March 7 2021

import pygame,sys,os

#文件位置
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"image") #图片
snd_folder=os.path.join(game_folder,"sound") #声音

size = WIDTH, HEIGHT = 800,600 #设置屏幕大小

BLACK = (0,0,0)#设置一种颜色

pygame.init() #初始化------这里开始是主程序

screen = pygame.display.set_mode(size) #应用屏幕大小
pygame.display.set_caption("游戏名")

#背景
background=pygame.image.load(os.path.join(img_folder,"galaxy.png")).convert()
background_rect=background.get_rect()

#怪物（以后会改）
monster = pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()
monster_rect=monster.get_rect()#在图片周围做切线形成一个矩形（这样图片就可以知道其位置和大小）
monster_speed = [1,1] #速度一次一个像素点

while True: #循环，一直获取用户的命令并执行
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    monster_rect = monster_rect.move(monster_speed[0], monster_speed[1]) #0是横向速度 1是纵向速度

    if monster_rect.left < 0 or monster_rect.right > WIDTH: #屏幕左上角是（0，0），如果怪物位置左边小于0或者大于宽的长度
        monster_speed[0] = -monster_speed[0] #反相速度，也就是反弹
    if monster_rect.top < 0 or monster_rect.bottom > HEIGHT: #上下同理
        monster_speed[1] = -monster_speed[1]

    screen.fill(BLACK)#每次怪物移动填充的颜色
    screen.blit(background,background_rect)#显示背景
    screen.blit(monster,monster_rect)#显示怪物
    
    pygame.display.update() #刷新屏幕