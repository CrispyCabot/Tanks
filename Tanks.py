#SnakeVsRoyale.py
import pygame
import os
import math
from random import randint, shuffle
from pygame.locals import *
import time

pygame.init()

width = 800
height = 500
size = .5
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tanks")

PATH = os.path.abspath(__file__)
PATH = PATH[0:-8] #-16 to chop off SnakeVsRoyale.py
font = pygame.font.SysFont('', 24)
bigFont = pygame.font.SysFont('', 30)

tankImg = pygame.image.load(PATH+'tank.png')
w, h = tankImg.get_rect().size
tankImg = pygame.transform.scale(tankImg, (w*size, h*size))

clock = pygame.time.Clock()

shotDelay = 200

class Tank:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        dirs = ['left', 'right', 'up', 'down']
        self.dir = dirs[randint(0,3)]
        self.move = '' #forward, backward, none
        self.kills = 0
        self.shots = []
        self.shotTimer = 0
    def getInfo(self):
        return [[self.x, self.y], self.angle, self.shots, self.shotTimer, self.kills]
    def getDir(self):
        self.dir = getattr(playerUpdates, self.name)(self.pos.copy(), self.bod.copy(), self.dir, info.copy())

class Shot:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir


def main():
    global length
    players = ['Chris']
    shuffle(players)
    counter = len(players)
    for i in range(0,counter-1):
        for x in range(0,5): #Number of repeated tanks
            players.append(players[i])
            pass
    tankList = []
    info = []
    tickRate = 5
    feed = []

    dirs = ['right', 'left', 'up', 'down']
    for i in players:
        tank = Tank()
        tankList.append(tank)

    playing = True
    tStart = time.time()
    while playing:
        clock.tick(tickRate)
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
                cont = False

        info = []
        for i in snakeList:
            info.append(i.getInfo())
        for i in snakeList:
            i.setDir(info.copy())
        #Check hit
        for i in snakeList:
            if i.alive:
                inf = i.getInfo()
                loc = inf[2]
                for x in info:
                    if loc in x[0]:
                        if inf[0]==x[0]: #Checks if it is itself
                            temp = x[0].copy()
                            temp.remove(loc)
                            if loc in temp: #Checks to see if the value is in the list twice
                                i.alive = False
                                snakeList.remove(i)
                                feed.append([i.name+' is out (Hit itself)', 0])
                                break
                        else: #Makes sure it isn't current position
                            i.alive = False
                            snakeList.remove(i)
                            feed.append([i.name+' is out (Hit Snake)', 0])
                            break
                if loc[0] < 0 or loc[0]>=width or loc[1]<0 or loc[1]>=height:
                    i.alive = False
                    snakeList.remove(i)
                    feed.append([i.name+' is out (Border)', 0])
                    break
        if (time.time()-tStart) > 1:
            length += 1
            tStart = time.time()
        if length > 3:
            tickRate = 30

        keys = pygame.key.get_pressed()
        for i in keys:
            if keys[pygame.K_ESCAPE]:
                cont = False
                playing = False
            elif keys[pygame.K_SPACE]:
                playing = False

        #Draw everything
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height)) #black background
        for i in snakeList:
            i.update(win)
        ycounter = 20
        for i in feed:
            text = bigFont.render(i[0], True, (0,0,0))
            loc = text.get_rect()
            loc.topleft = (20,ycounter)
            w, h = loc.size
            pygame.draw.rect(win, (255,255,255), pygame.Rect(loc.x-5, loc.y-5, w+10, h+10))
            win.blit(text, loc)
            ycounter+=h+15
            i[1] += 4
            if i[1] > 200:
                feed.remove(i)
        pygame.draw.rect(win, (255,255,255), pygame.Rect(0,0,width,height), 1) #White border
        pygame.display.update()

class playerUpdates:
    def Chris(info):
        return 'right'
