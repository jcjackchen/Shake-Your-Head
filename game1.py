#-*-coding:utf-8-*-
import pygame
import time
import threading
from sys import exit
from pygame.locals import *
from Bullet import Bullet
from Enemy import Enemy
from Player import Player
import random
import face_recognition
import cv2
from multiprocessing import Pool, Process, Queue, Pipe, Array, Lock


# 设置游戏屏幕大小
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
counter = 1

def determine_action(q, q1):
    prev_y = None
    prev_x = None
    global counter
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        sframe = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(sframe)
        if len(face_locations) > 0:
            #print face_locations
            top, right, bottom, left = face_locations[0]
            #print face_locations
            y = (top + bottom) / 2
            x = (right + left) / 2
            if prev_y is None:
                prev_y = y
                prev_x = x
            tanx = x - prev_x
            tany = y - prev_y
            #print tanx, tany
            q.put([tanx, tany])
            prev_y = y
            prev_x = x


if __name__ == '__main__':
    status = True
    while status:
        counter = 1

        # 初始化 pygame
        pygame.init()

        # 设置游戏界面大小、背景图片及标题
        # 游戏界面像素大小
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # 游戏界面标题
        pygame.display.set_caption('治疗劲椎病')

        # 背景图
        # background = pygame.image.load('resources/image/background.png').convert()
        background = pygame.image.load('resources/image/background.jpg')

        # Game Over 的背景图
        game_over = pygame.image.load('resources/image/gameover.png')

        # 飞机及子弹图片集合
        plane_img = pygame.image.load('resources/image/shoot.png')

        plane_img2 = pygame.image.load('resources/image/hero.png')

        # 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
        player_rect = []
        player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家飞机图片
        player_rect.append(pygame.Rect(165, 360, 102, 126))
        player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片
        player_rect.append(pygame.Rect(330, 624, 102, 126))
        player_rect.append(pygame.Rect(330, 498, 102, 126))
        player_rect.append(pygame.Rect(432, 624, 102, 126))
        player_pos = [200, 600]
        player = Player(plane_img2, plane_img, player_rect, player_pos,SCREEN_WIDTH,SCREEN_HEIGHT)

        # 子弹图片
        bullet_rect = pygame.Rect(1004, 987, 9, 21)
        bullet_img = plane_img.subsurface(bullet_rect)

        # 敌机不同状态的图片列表，多张图片展示为动画效果
        enemy1_rect = pygame.Rect(534, 612, 57, 43)
        # enemy1_img = plane_img.subsurface(enemy1_rect)
        enemy1_img = pygame.image.load('resources/image/enemy.png')
        enemy1_down_imgs = []
        # enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
        enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
        enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
        enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

        #存储敌机，管理多个对象
        enemies1 = pygame.sprite.Group()

        # 存储被击毁的飞机，用来渲染击毁动画
        enemies_down = pygame.sprite.Group()

        # 初始化射击及敌机移动频率
        shoot_frequency = 0
        enemy_frequency = 0

        # 玩家飞机被击中后的效果处理
        player_down_index = 16

        # 初始化分数
        score = 0

        # 游戏循环帧率设置
        clock = pygame.time.Clock()

        # 判断游戏循环退出的参数
        running = True


        diff_y = None
        diff_x = None

        q = Queue()
        q1 = Queue()

        threads = []
        thread = []
        threadnum = 0
        getnum = 0
        start = -1
        p = Process(target=determine_action, args=(q, q1))
        p.start()

        # 游戏主循环
        while running:
            # 控制游戏最大帧率为 60
            clock.tick(60)
            counter +=1

            # 生成子弹，需要控制发射频率
            # 首先判断玩家飞机没有被击中
            if not player.is_hit:
                if shoot_frequency % 5 == 0:
                    player.shoot(bullet_img)
                shoot_frequency += 1
                if shoot_frequency >= 10:
                    shoot_frequency = 0

            # 生成敌机，需要控制生成频率
            if enemy_frequency % 15 == 0:
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
                enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
                enemies1.add(enemy1)
            enemy_frequency += 1
            if enemy_frequency >= 100:
                enemy_frequency = 0

            for bullet in player.bullets:
                # 以固定速度移动子弹
                bullet.move()
                # 移动出屏幕后删除子弹
                if bullet.rect.bottom < 0:
                    player.bullets.remove(bullet)

            for enemy in enemies1:
                #2. 移动敌机
                enemy.move()
                #3. 敌机与玩家飞机碰撞效果处理
                if pygame.sprite.collide_circle(enemy, player):
                    enemies_down.add(enemy)
                    enemies1.remove(enemy)
                    player.is_hit = True
                    break
                #4. 移动出屏幕后删除飞机
                if enemy.rect.top < 0:
                    enemies1.remove(enemy)

            #敌机被子弹击中效果处理
            # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
            enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
            for enemy_down in enemies1_down:
                enemies_down.add(enemy_down)

            # 绘制背景
            screen.fill(0)
            screen.blit(background, (0, 0))

            # 绘制玩家飞机
            if not player.is_hit:
                screen.blit(player.image[player.img_index], player.rect)
                # 更换图片索引使飞机有动画效果
                # player.img_index = shoot_frequency // 8
            else:
                # 玩家飞机被击中后的效果处理
                player.img_index = player_down_index // 8
                screen.blit(player.image[player.img_index], player.rect)
                player_down_index += 1
                if player_down_index > 47:
                    # 击中效果处理完成后游戏结束
                    running = False

            # 敌机被子弹击中效果显示
            for enemy_down in enemies_down:
                if enemy_down.down_index == 0:
                    pass
                if enemy_down.down_index > 5:
                    enemies_down.remove(enemy_down)
                    score += 1000
                    continue
                screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
                enemy_down.down_index += 1

            # 显示子弹
            player.bullets.draw(screen)
            # 显示敌机
            enemies1.draw(screen)

            # 绘制得分
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(str(score), True, (128, 128, 128))
            text_rect = score_text.get_rect()
            text_rect.topleft = [10, 10]
            screen.blit(score_text, text_rect)

            # 更新屏幕
            pygame.display.update()

            # 处理游戏退出
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # 获取键盘事件（上下左右按键)
            # p = Process(target=determine_action,args=(action_buffer,prev_x,prev_y))
            # p.start()
            key_pressed = pygame.key.get_pressed()
            #if counter % 10 == 0:
            [diff_x, diff_y] = q.get()

            #print diff_x, diff_y

            # 处理键盘事件（移动飞机的位置）
            if key_pressed[K_w] or key_pressed[K_UP] or diff_y < 0:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN] or diff_y > 0:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT] or diff_x > 0:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT] or diff_x < 0:
                player.moveRight()

        # 游戏 Game Over 后显示最终得分
        font = pygame.font.Font(None, 48)
        text = font.render('Score: '+ str(score), True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery - 124
        screen.blit(game_over, (-45, 0))
        screen.blit(text, text_rect)
        p.terminate()

    # 显示得分并处理游戏退出
        while True:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_RETURN]:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    status = False
                    pygame.quit()
                    exit()
            pygame.display.update()
            p.join()
            p.terminate()