﻿#-*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame
from pygame.locals import *
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

# 글 머리 기호 클래스
class Bullet(pygame.sprite.Sprite):
	def __init__(self, bullet_img, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 10
	
	def move(self):
		self.rect.top -= self.speed
		
	def enemy_move(self):
		self.rect.top += 7

# 플레이어 등급
class Player(pygame.sprite.Sprite):
	def __init__(self, plane_img, player_rect, init_pos):
		pygame.sprite.Sprite.__init__(self)
		# 플레이어 오브젝트 스프라이트 목록을 저장하는 데 사용됩니다.
		self.image = []
		for i in range(len(player_rect)):
			self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
		# 그림의 사각형을 초기화하십시오.
		self.rect = player_rect[0]
		# 사각형의 왼쪽 위 모서리 좌표를 초기화합니다.
		self.rect.topleft = init_pos
		# 초기 플레이어 속도, 여기에 특정 값이 있습니다.
		self.speed = 8
		# 플레이어의 항공기에 의해 발사 된 총알의 컬렉션
		self.bullets = pygame.sprite.Group()
		# 플레이어 마법사 그림 색인
		self.img_index = 0
		# 플레이어가 맞았는지 여부
		self.is_hit = False                             
	
	# 플레이어가 총알을 발사했을때의 이벤트
	def shoot(self, bullet_img):
		bullet = Bullet(bullet_img, self.rect.midtop)
		self.bullets.add(bullet)
	
	#플레이어가 상 하 좌 우 움직이게 되면 어느정도 이동하는지 계산하는 부분
	def moveUp(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		else:
			self.rect.top -= self.speed
		
	def moveDown(self):
		if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT - self.rect.height
		else:
			self.rect.top += self.speed

	def moveLeft(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		else:
			self.rect.left -= self.speed
	
	def moveRight(self):
		if self.rect.left >= SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH - self.rect.width
		else:
			self.rect.left += self.speed

# 적 클래스
class Enemy(pygame.sprite.Sprite):
	def __init__(self, enemy_img, enemy_down_imgs, init_pos):
	# 적에 대한 기본 값 설정
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_img
		self.rect = self.image.get_rect()
		self.rect.topleft = init_pos
		self.down_imgs = enemy_down_imgs
		self.speed = 2
		self.down_index = 0
		self.bullets = pygame.sprite.Group()
	   
	# 플레이어가 총알을 발사했을때의 이벤트
	def shoot(self, bullet_img):
		bullet = Bullet(bullet_img, self.rect.midbottom)
		self.bullets.add(bullet)
	
	#적의 움직임 이벤트
	def move(self):
		self.rect.top += self.speed


class Menu(pygame.sprite.Sprite):
	def __init__(self, background, screen):
		pygame.sprite.Sprite.__init__(self)
		self.image = background
		self.menus = []
		self.menus.append("Start")
		self.menus.append("Exit")
		self.focused = 0
		self.font = pygame.font.Font(None, 48)
		self.item = list()
		self.item_rect = list()
		self.offsety = 24
		self.screen = screen
		self.screen.blit(self.image, (0, 0))
		print("menu init")
				
	def select(self, key):
		print("waiting event")
		if key == K_UP or key == K_w:
			print("Up")
			self.moveUp()
			self.updateMenu()
		if key == K_s or key == K_DOWN:
			print("Down")
			self.moveDown()
			self.updateMenu()
		if key == K_RETURN:
			print("Return")
			if self.focused == self.menus.index("Start"):
				return 1
			elif self.focused == self.menus.index("Exit"):
				return 2
		print("no event")
		return 0

	def moveUp(self):
		self.focused = (self.focused+1)%2

	def moveDown(self):
		self.focused = (self.focused-1)%2

	def updateMenu(self):
		print("updateMenu")
		del self.item
		del self.item_rect
		self.item = list()
		self.item_rect = list()
		i = 0
		while i<len(self.menus):
			m = self.menus[i]
			if self.focused == i:
				text = self.font.render(m, True, (0,255,0))
			else:
				text = self.font.render(m, True, (0,0,255))
			self.item.append(text)
			i = i+1

		for i in self.item:
			rect = i.get_rect()
			self.item_rect.append(rect)

		for i in self.item_rect:
			i.centerx = self.screen.get_rect().centerx
			i.centery = self.screen.get_rect().centery +self.offsety
			self.offsety += 48
		self.offsety = 24
		i = 0
		while i < len(self.item):
			self.screen.blit(self.item[i], self.item_rect[i])
			i+=1
		pygame.display.update()
