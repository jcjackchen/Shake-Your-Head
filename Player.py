#-*-coding:utf-8-*-
# -*- coding: utf-8 -*-
import pygame
from Bullet import Bullet

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self,plane_img, player_rect, init_pos,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        # self.image[0] = self.image[2] = self.image[3] =self.image[4] = plane_img2
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 5                                 # 初始化玩家飞机速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家飞机图片索引
        self.is_hit = False                             # 玩家是否被击中
        self.width = width
        self.height = height

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    # 向上移动，需要判断边界
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # 向下移动，需要判断边界
    def moveDown(self):
        if self.rect.top >= self.height - self.rect.height:
            self.rect.top = self.height - self.rect.height
        else:
            self.rect.top += self.speed

    # 向左移动，需要判断边界
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动，需要判断边界        
    def moveRight(self):
        if self.rect.left >= self.width- self.rect.width:
            self.rect.left = self.width- self.rect.width
        else:
            self.rect.left += self.speed