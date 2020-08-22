import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import random
import time
pygame.init()

RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(77, 73, 73)

time_start = time.time()
size = (505,525)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
global done

mine_list = []
vis = []
font = pygame.font.SysFont("Calibri.ttf",25)

class Quad():
	def __init__(self,pos,side):
		self.color = BLACK
		self.pos = pos
		self.side = side
		self.rect = Rect(pos,side)
		self.score = 0
		self.mine = False
		self.visible =False
		self.flag = False

def draw(list):
	for i in list:
		for j in i:
			pygame.draw.rect(screen,j.color,j.rect)

def show_val():
	#font = pygame.font.SysFont("Calibri.ttf",25)
	text = font.render("0",True,BLACK,WHITE)
	textRect = text.get_rect()
	for i in mine_list:
		for j in i:
			if j.visible and not j.flag:
				text = font.render(str(j.score),True,WHITE,GREY)
				textRect.center = (j.rect.x + 23 ,j.rect.y + 24)
				screen.blit(text,textRect)

def show_score():
	time_dif = int(time.time() - time_start)
	minutes = time_dif//60
	seconds = time_dif - (minutes*60)
	num_flags = 0
	for i in mine_list:
		for j in i:
			if j.color == GREEN:
				num_flags+=1


	#game_font = pygame.font.SysFont("Calibri.ttf",20)
	flag_text = font.render("Flags : " + str(num_flags),True,GREY,WHITE)
	time_text = font.render("Time : " + str(minutes) + ":" + str(seconds),True,GREY,WHITE)
	textRect1 = flag_text.get_rect()
	textRect2 = time_text.get_rect()
	textRect1.topleft = (5,503)
	textRect2.topleft = (420,503)
	screen.blit(flag_text,textRect1)
	screen.blit(time_text,textRect2)


def game_over():

	game_text = font.render("00",True,BLACK,WHITE)
	textRect = game_text.get_rect()

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		draw(mine_list)
		for i in mine_list:
			for j in i:
				if j.score != -1 and j.visible == True and not j.flag:
					game_text = font.render(str(j.score),True,WHITE,GREY)
					textRect.center = (j.rect.x + 23,j.rect.y + 24)
					screen.blit(game_text,textRect)
				if j.score != -1 and j.visible == False and not j.flag:
					game_text = font.render(str(j.score),True,WHITE,BLACK)
					textRect.center = (j.rect.x + 23,j.rect.y + 24)
					screen.blit(game_text,textRect)
				if j.score == -1 and not j.flag:
					j.color = RED
				if j.flag and not j.mine:
					j.color = GREEN
					game_text = font.render(str(j.score),True,WHITE,GREEN)
					textRect.center = (j.rect.x + 23,j.rect.y + 24)
					screen.blit(game_text,textRect)
				if j.flag and j.mine:
					j.color = GREEN

		pygame.display.flip()
		clock.tick(60)


def mine_placement():
	mines = 0
	for i in range(10):
		mine_list.append([])
		for j in range(10):
			quad = Quad((i*50,j*50),(45,45))
			mine_list[i].append(quad)

	while mines<10:
		mine_loc = [random.randrange(10),random.randrange(10)]
		if not mine_list[mine_loc[0]][mine_loc[1]].mine:
			mine_list[mine_loc[0]][mine_loc[1]].mine = True
			mine_list[mine_loc[0]][mine_loc[1]].score = -1
			mines+=1


def adjacent_mines():
	for i in range(10):
		for j in range(10):
			neighb_num = 0
			if mine_list[i][j].score != -1:
				if i>0 and j>0:
					if mine_list[i-1][j-1].mine == True:
						neighb_num+=1

				if i>0 :
					if mine_list[i-1][j].mine == True:
						neighb_num+=1

				if i>0 and j<9:
					if mine_list[i-1][j+1].mine == True:
						neighb_num+=1

				if j>0:
					if mine_list[i][j-1].mine == True:
						neighb_num+=1

				if j<9:
					if mine_list[i][j+1].mine == True:
						neighb_num+=1

				if j>0 and i<9:
					if mine_list[i+1][j-1].mine == True:
						neighb_num+=1

				if i<9:
					if mine_list[i+1][j].mine == True:
						neighb_num+=1

				if i<9 and j<9:
					if mine_list[i+1][j+1].mine == True:
						neighb_num+=1

				mine_list[i][j].score = neighb_num

def update(r,c):
	if [r,c] not in vis:
		vis.append([r,c])
		if mine_list[r][c].score == -1:
			mine_list[r][c].color = RED
			game_over()


		if mine_list[r][c].score == 0:
			mine_list[r][c].visible = True
			mine_list[r][c].color = GREY

			if r>0:
				update(r-1,c)
			if r<9:
				update(r+1,c)
			if c>0:
				update(r,c-1)
			if c<9:
				update(r,c+1)
			if r>0 and c>0:
				update(r-1,c-1)
			if r>0 and c<9:
				update(r-1,c+1)
			if r<9 and c>0:
				update(r+1,c-1)
			if r<9 and c<9:
				update(r+1,c+1)

		if mine_list[r][c].score != 0 and mine_list[r][c].score != -1:
			mine_list[r][c].visible = True
			mine_list[r][c].color = GREY

def check_game():
	points = 0
	flags = 0
	for i in mine_list:
		for j in i:
			if j.color == GREEN:
				flags+=1
			if j.color==GREEN and j.mine and points < 10 :
				points+=1
			if points==10 and flags==10:
				game_won()
				return True
			if done:
				return True

def game_won():
	print(" you won")

mine_placement()
adjacent_mines()

done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			new_pos = [i/50 for i in pos]
			if event.button == 1:
				update(int(new_pos[0]),int(new_pos[1]))
			if event.button == 3:
				if not mine_list[int(new_pos[0])][int(new_pos[1])].flag and not mine_list[int(new_pos[0])][int(new_pos[1])].visible:
					mine_list[int(new_pos[0])][int(new_pos[1])].color = GREEN
					mine_list[int(new_pos[0])][int(new_pos[1])].flag = True
				elif mine_list[int(new_pos[0])][int(new_pos[1])].flag and not mine_list[int(new_pos[0])][int(new_pos[1])].visible:
					mine_list[int(new_pos[0])][int(new_pos[1])].color = BLACK
					mine_list[int(new_pos[0])][int(new_pos[1])].flag = False


	screen.fill(WHITE)
	draw(mine_list)
	show_val()
	show_score()
	done = check_game()

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
