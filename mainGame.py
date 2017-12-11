# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""
# pygame 모듈을 import
import pygame
from sys import exit
# pygame.locals 하위 모듈을 import
from pygame.locals import *
from gameRole import *
import random



# 게임초기화
# pyGame 라이브러리 초기화
pygame.init()
# 해상도 조정 SCREEN_WIDTH, SCREEN_HEIGHT 는 Role.py 파일에 존재
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 타이틀바 텍스트 설정 (비행기 전쟁)
pygame.display.set_caption('飞机大战')

# 게임 사운드 로드
# 사운드 파일을 로딩한다 pygame.mixer.Sound
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
# 사운드 볼륨 조정
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
# 반복해서 플레이하는 경우 (BGM)
pygame.mixer.music.load('resources/sound/game_music.wav')
# BGM 재생
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 배경 로드
# 이미지 파일 그리기 -> pygame.image.load
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

# ?? 왜 이것만 변수로 빼서 로드 했는지 이유를 알 수 없음
filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 플레이어 관련 매개 변수 설정 player_rect
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
# Player Elves 그림 영역
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     
# 플레이어가 스프라이트 그림 영역을 분해합니다.
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 총알 객체가 사용하는 곡면 관련 매개 변수를 정의합니다.
bullet_rect = pygame.Rect(1004, 987, 9, 21)
# 총알 부분의 이미지를 잘라냄
bullet_img = plane_img.subsurface(bullet_rect)

# 적 항공기가 사용하는 지표 관련 매개 변수 정의
enemy1_rect = pygame.Rect(534, 612, 57, 43)
# 적항공기 이미지 잘라냄
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

#적 항공기 그룹
enemies1 = pygame.sprite.Group()

# 난파선 애니메이션을 렌더링하는 데 사용 된 파괴 된 항공기 저장
enemies_down = pygame.sprite.Group()

#사격 횟수 변수
shoot_frequency = 0
#적 개수 변수
enemy_frequency = 0

#적사격 횟수 변수
enemy_shoot_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True
ismenu = 0

#시작 화면 변수
menu = Menu(background, screen)
menu.updateMenu()	

# 게임의 최대 프레임 속도를 60으로 제어
clock.tick(60)
def endPage():
	#게임내에 표시 되는 점수 등 location 설정
	font = pygame.font.Font(None, 48)
	text = font.render('Score: '+ str(score) + ' Exit : q', True, (255, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 24
	screen.blit(game_over, (0, 0))
	screen.blit(text, text_rect)
    
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		key_pressed = pygame.key.get_pressed()
		if key_pressed[K_q]:
			pygame.quit()
			exit()

		if ismenu == 0:
			if event.type == KEYDOWN:
				ismenu = menu.select(event.key)
		elif ismenu == 1:
			running == True
		elif ismenu == 2:
			pygame.quit()
			exit()
		else:

			while running:
				# 사격 횟수 제어 및 총알 발사
				clock.tick(60)
				if not player.is_hit:
					if shoot_frequency % 15 == 0:
						# 총알 발사 사운드
						bullet_sound.play()
					# bullet_img == 총알 이미지
						player.shoot(bullet_img)
					shoot_frequency += 1
					if shoot_frequency >= 15:
						shoot_frequency = 0

				# 적 항공기 생성
				if enemy_frequency % 50 == 0:
					#랜덤한 위치의 적 항공기 좌표 생성 width만 임의 , height는 맨끝
					enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
					# 적 class 생성 좌표, 이미지, 적이 침몰했을때 이미지
					enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
					# 적 그룹에 추가
					enemies1.add(enemy1)

				if enemy_shoot_frequency % 35 == 0:
					for enemy in enemies1:    
						#(추가)
						enemy.shoot(bullet_img)
				enemy_shoot_frequency += 1
				if enemy_shoot_frequency >= 35:
					enemy_shoot_frequency = 0

				# 글 머리 기호가 창 밖으로 나가면 삭제하십시오. (추가)
				for enemy in enemies1:
					for bullet in enemy.bullets:
						bullet.enemy_move()
						if bullet.rect.bottom < 0:
							enemy.bullets.remove(bullet)
									
							
				#적 항공기 개수 변수에 추가
				enemy_frequency += 1
				if enemy_frequency >= 100:
					enemy_frequency = 0

				# 글 머리 기호가 창 밖으로 나가면 삭제하십시오.
				for bullet in player.bullets:
					bullet.move()
					if bullet.rect.bottom < 0:
						player.bullets.remove(bullet)

				# 적기가 창 범위를 벗어난 경우 이동하여 삭제합니다.
				for enemy in enemies1:
				# 적 항공기 이동
					enemy.move()

					# 플레이어가 맞았는지 확인
					if pygame.sprite.collide_circle(enemy, player):
						enemies_down.add(enemy)
						# 적항공기 전체 삭제
						enemies1.remove(enemy)
						# player hit 변수 변경
						player.is_hit = True
						# 게임 오버 사운드 재생
						game_over_sound.play()
						break
					#추가
					hits = pygame.sprite.spritecollide(player, enemy.bullets, True)
					if hits:
						# 적항공기 전체 삭제
						enemies1.remove(enemy)
						# player hit 변수 변경
						player.is_hit = True
						# 게임 오버 사운드 재생
						game_over_sound.play()
						break
					# 스크린을 벗어났을경우 해당 적 삭제
					if enemy.rect.top > SCREEN_HEIGHT:
						enemies1.remove(enemy)	

				# 적의 비행기에 의해 맞을 것입니다 개체는 적군의 파괴에 추가, 난파 애니메이션을 렌더링하는 데 사용됩니다
				enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
				for enemy_down in enemies1_down:
				# 격파한 적 항공기 목록에 추가		
					enemies_down.add(enemy_down)

				# 배경 그리기
				screen.fill(0)
				screen.blit(background, (0, 0))

				# 플레이어 비행기를 그립니다.
				if not player.is_hit:
					screen.blit(player.image[player.img_index], player.rect)
					# 항공기가 애니메이션 효과를 낼 수 있도록 그림 색인을 변경하십시오
					player.img_index = shoot_frequency // 8
				else:
					player.img_index = player_down_index // 8
					screen.blit(player.image[player.img_index], player.rect)
					player_down_index += 1
					if player_down_index > 47:
						running = False

				# 잔해 애니메이션 그리기
				for enemy_down in enemies_down:
					if enemy_down.down_index == 0:
						enemy1_down_sound.play()
					if enemy_down.down_index > 7:
						enemies_down.remove(enemy_down)
						score += 1000
						continue
					screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
					enemy_down.down_index += 1

				# 총알과 적기 그리기
				player.bullets.draw(screen)
				for enemy in enemies1:
					enemy.bullets.draw(screen)
				enemies1.draw(screen)

				# 점수 뽑기
				score_font = pygame.font.Font(None, 36)
				score_text = score_font.render(str(score), True, (128, 128, 128))
				text_rect = score_text.get_rect()
				text_rect.topleft = [10, 10]
				screen.blit(score_text, text_rect)

				# 화면 업데이트
				pygame.display.update()
				
				# 나가기 이벤트
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						exit()

				# 사용자가 죽었을 경우 자동 나가기 실행
				#if player.is_hit :
						#pygame.quit()
						#exit()
								
				# 키보드 이벤트 가져오기
				key_pressed = pygame.key.get_pressed()
				# 플레이어가 죽지 않았을 때 키보드 키에 따라 플레이어 이동
				if not player.is_hit:
					if key_pressed[K_w] or key_pressed[K_UP]:
						player.moveUp()
					if key_pressed[K_s] or key_pressed[K_DOWN]:
						player.moveDown()
					if key_pressed[K_a] or key_pressed[K_LEFT]:
						player.moveLeft()
					if key_pressed[K_d] or key_pressed[K_RIGHT]:
						player.moveRight()
			endPage()



	pygame.display.update()
