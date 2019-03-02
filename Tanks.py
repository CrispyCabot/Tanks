#SnakeVsRoyale.py
import pygame
import os
from math import cos, sin, radians
from random import randint, shuffle
from pygame.locals import *
import time

pygame.init()

width = 800
height = 500
size = .1
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Tanks")

PATH = os.path.abspath(__file__)
PATH = PATH[0:-8] #-16 to chop off SnakeVsRoyale.py
font = pygame.font.SysFont('', 24)
bigFont = pygame.font.SysFont('', 30)

tankImg = pygame.image.load(PATH+'tank.png')
shotImg = pygame.image.load(PATH+'shot.png')
w, h = tankImg.get_rect().size
tankImg = pygame.transform.scale(tankImg, (int(w*size), int(h*size)))
tankWidth, tankHeight = tankImg.get_rect().size
w, h = shotImg.get_rect().size
shotImg = pygame.transform.scale(shotImg, (int(w*size*.4,), int(h*size*.4)))

clock = pygame.time.Clock()

turnSpeed = 5
moveSpeed = 5
shotSpeed = 10

class Tank:
    def __init__(self, x, y, angle, name):
        self.image = pygame.image.load(PATH+os.path.join('tankColors', 'tank'+str(randint(1,35))+'.png'))
        w, h = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (int(w*size), int(h*size)))
        self.x = x
        self.y = y
        self.angle = angle
        dirs = ['right', 'left']
        self.dir = ''
        self.move = '' #forward, backward, none
        self.kills = 0
        self.shots = []
        self.shotTimer = 0
        self.bullets = 5
        self.alive = True
        self.name = name
        self.shoot = False
    def getInfo(self):
        return [[self.x, self.y], self.angle, self.shots, self.shotTimer, self.kills]
    def setDir(self, info):
        self.dir, self.move, self.shoot = getattr(playerUpdates, self.name)([self.x, self.y], self.dir, self.move, info.copy())
    def update(self, win):
        if self.shoot and self.bullets > 0:
            self.bullets -= 1
            self.shots.append(Shot(self.x, self.y, self.angle))
        for i in self.shots:
            if i.update(win):
                self.shots.remove(i)
        self.shotTimer += 1
        if self.dir == 'left':
            self.angle += turnSpeed
            if self.angle > 360:
                self.angle -= 360
        elif self.dir == 'right':
            self.angle -= turnSpeed
            if self.angle < 0:
                self.angle += 360
        if self.move == 'forward':
            if 0+tankHeight/2 < self.x + cos(radians(self.angle))*moveSpeed < width-tankHeight/2: #May need to use height instead of width - use the smallest one
                self.x += cos(radians(self.angle))*moveSpeed
            if 0+tankHeight/2 < self.y - sin(radians(self.angle))*moveSpeed < height-tankHeight/2:
                self.y -= sin(radians(self.angle))*moveSpeed
        elif self.move == 'backward':
            if 0+tankHeight < self.x - cos(radians(self.angle))*moveSpeed < width-tankHeight:
                self.x -= cos(radians(self.angle))*moveSpeed
            if 0+tankHeight < self.y + sin(radians(self.angle))*moveSpeed < height-tankHeight:
                self.y += sin(radians(self.angle))*moveSpeed
        img = pygame.transform.rotate(self.image, self.angle)
        pos = img.get_rect()
        pos.center = (self.x, self.y)
        win.blit(img, pos)
        text = font.render(self.name, True, (0,0,0))
        pos = text.get_rect()
        pos.center = (self.x, self.y-tankHeight)
        w, h = pos.size
        pygame.draw.rect(win, (255,255,255), pygame.Rect(pos.x, pos.y, w, h))
        win.blit(text, pos)

class Shot:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    def update(self, win):
        img = pygame.transform.rotate(shotImg, self.angle)
        pos = img.get_rect()
        pos.center = (self.x, self.y)
        win.blit(img, pos)
        self.x += cos(radians(self.angle))*shotSpeed
        self.y -= sin(radians(self.angle))*shotSpeed
        if self.x < -50 or self.x > width+50 or self.y > height+50 or self.y < -50:
            return True


def main():
    players = ['Keys']
    shuffle(players)
    counter = len(players)
    for i in range(0,counter):
        for x in range(0,4): #Number of repeated tanks
            players.append(players[i])
            pass
    tankList = []
    info = []
    tickRate = 30
    feed = []

    for i in players:
        tank = Tank(randint(50,width-50), randint(50,height-50), randint(0,360), i)
        tankList.append(tank)

    playing = True
    tStart = time.time()
    while playing:
        clock.tick(tickRate)
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
        global keys
        keys = pygame.key.get_pressed()
        for i in keys:
            if keys[pygame.K_ESCAPE]:
                playing = False

        if time.time() - tStart > 3:
            tStart = time.time()
            for i in tankList:
                i.bullets += 1

        info = []
        for i in tankList:
            info.append(i.getInfo())
        for i in tankList:
            i.setDir(info.copy())
        #Check hit
        for i in tankList:
            tank = [i.x, i.y]
            dead = False
            for x in info:
                for y in x[2]: #Shot list
                    shot = [y.x, y.y]
                    collision = False
                    if abs(shot[0]-tank[0]) < tankHeight/2 and abs(shot[1]-tank[1]) < tankHeight/2:
                        collision = True
                    if collision and not(x[0] == [i.x, i.y]): #makes sure it isn't own shot
                        feed.append([i.name + ' is out', 0])
                        x[2].remove(y)
                        dead = True
                        tankList.remove(i)
                        break
                if dead:
                    break
            if dead:
                break


        #Draw everything
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height)) #black background
        for i in tankList:
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
        #pygame.draw.rect(win, (255,255,255), pygame.Rect(0,0,width,height), 1) #White border
        pygame.display.update()

class playerUpdates:
    #Return 'right' or 'left' , 'forward' or 'backward' , True or False
    #You CAN return nothing for the first two, but must return True or False for the last part
    def Chris(loc, dir, move, info):
        lr = ['left', 'right', '', '']
        fb = ['forward', 'backward', '']
        if randint(0,20) == 1:
            return lr[randint(0,3)], fb[randint(0,2)], True
        else:
            return dir, move, True
    def Keys(loc, dir, move, info):
        global keys
        dir1, dir2 = '', ''
        if keys[pygame.K_UP]:
            dir1 = 'forward'
        if keys[pygame.K_DOWN]:
            dir1 = 'backward'
        if keys[pygame.K_LEFT]:
            dir2 = 'left'
        if keys[pygame.K_RIGHT]:
            dir2 = 'right'
        return dir2, dir1, True

main()
