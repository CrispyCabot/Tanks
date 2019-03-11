#Tanks.py
import pygame
import os
from math import *
from random import randint, shuffle
from pygame.locals import *
import time

pygame.init()

width = 800
height = 500
size = .07
win = pygame.display.set_mode((width+200,height)) #additional 200 to width for scoreboard
pygame.display.set_caption("Tanks")

PATH = os.path.abspath(__file__) #This gets the whole path so like: /Users/user/folder/Tanks/Tanks.py
PATH = PATH[0:-8] #-8 to chop off Tanks.py
#Using this PATH variables makes loading things less error prone
font = pygame.font.SysFont('', 24) #Loads default font at size 24
bigFont = pygame.font.SysFont('', 30) #Same but size 30

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
    shotDelay = 5
    def __init__(self, x, y, angle, name):
        self.image = pygame.image.load(PATH+os.path.join('tankColors', 'tank'+str(randint(1,35))+'.png'))
        w, h = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (int(w*size), int(h*size)))
        self.x = x
        self.y = y
        self.angle = angle
        self.dir = ''
        self.move = '' #forward, backward, none
        self.kills = 0
        self.shots = []
        self.delay = 0
        self.bullets = 0
        self.alive = True
        self.name = name
        self.shoot = False
    def getInfo(self):
        return [[self.x, self.y], self.angle, self.shots, self.bullets, self.kills]
    def setDir(self, info):
        self.dir, self.move, self.shoot = getattr(playerUpdates, self.name)([self.x, self.y], self.dir, self.move, self.angle, self.bullets, info.copy())
    def update(self, win):
        self.delay += 1
        if self.alive:
            if self.shoot and self.bullets > 0 and self.delay > Tank.shotDelay:
                self.bullets -= 1
                self.delay = 0
                self.shots.append(Shot(self.x, self.y, self.angle))
            for i in self.shots:
                if i.update(win):
                    self.shots.remove(i)
            if self.dir == 'left':
                self.angle += turnSpeed
                if self.angle > 360:
                    self.angle -= 360
            elif self.dir == 'right':
                self.angle -= turnSpeed
                if self.angle < 0:
                    self.angle += 360
            if self.dir == 'sright':
                self.angle -= 1
            if self.dir == 'sleft':
                self.angle += 1
            if self.move == 'forward':
                if 0+tankHeight/2 < self.x + cos(radians(self.angle))*moveSpeed < width-tankHeight/2: #May need to use height instead of width - use the smallest one
                    self.x += cos(radians(self.angle))*moveSpeed
                if 0+tankHeight/2 < self.y - sin(radians(self.angle))*moveSpeed < height-tankHeight/2:
                    self.y -= sin(radians(self.angle))*moveSpeed
            elif self.move == 'backward':
                if 0+tankHeight/2 < self.x - cos(radians(self.angle))*moveSpeed < width-tankHeight/2:
                    self.x -= cos(radians(self.angle))*moveSpeed
                if 0+tankHeight/2 < self.y + sin(radians(self.angle))*moveSpeed < height-tankHeight/2:
                    self.y += sin(radians(self.angle))*moveSpeed
            img = pygame.transform.rotate(self.image, self.angle)
            pos = img.get_rect()
            pos.center = (self.x, self.y)
            win.blit(img, pos)
            text = font.render(self.name+' '+ str(self.kills), True, (0,0,0))
            pos = text.get_rect()
            pos.center = (self.x, self.y-tankHeight)
            w, h = pos.size
            pygame.draw.rect(win, (255,255,255), pygame.Rect(pos.x, pos.y, w, h))
            win.blit(text, pos)
        else:
            self.x = -1000
            self.y = -1000
            for i in self.shots:
                if i.update(win):
                    self.shots.remove(i)
            if len(self.shots) == 0:
                return True

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
    def dist(p1, p2):
        return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2) #distance formula
    global end
    players = ['Rando', 'Chris', 'Rando', 'Keys']
    shuffle(players)
    counter = len(players)
    for i in range(0,counter):
        for x in range(1,5): #Number of repeated tanks
            players.append(players[i])
            pass
    tankList = []
    info = []
    tickRate = 30
    feed = []
    deadTanks = []
    giveBulletDelay = 3
    initTime = time.time()

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
                end = False
        global keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            playing = False
            end = False
        if keys[pygame.K_r]:
            playing = False

        if time.time() - tStart > giveBulletDelay:
            tStart = time.time()
            for i in tankList:
                i.bullets += 1
        if time.time()-initTime > 10:
            giveBulletDelay = 2.5
        if time.time()-initTime > 20:
            giveBulletDelay = 2
        if time.time()-initTime > 30:
            giveBulletDelay = 1.5
        if time.time()-initTime > 40:
            giveBulletDelay = 1
        if time.time()-initTime > 50:
            giveBulletDelay = .5
        if time.time()-initTime > 60:
            giveBulletDelay = 0

        info = []
        for i in tankList:
            info.append(i.getInfo())
        for i in tankList:
            i.setDir(info.copy())
        #Check hit
        for i in tankList:
            tank = [i.x, i.y]
            dead = False
            for x in tankList:
                for y in x.shots: #Shot list
                    shot = [y.x, y.y]
                    collision = False
                    if dist(shot, tank) < tankHeight/2:
                        collision = True
                    if collision and not([x.x, x.y] == [i.x, i.y]): #makes sure it isn't own shot
                        feed.append([i.name + ' is out', 0])
                        x.shots.remove(y)
                        x.kills += 1
                        dead = True
                        i.alive = False
                        break
                if dead:
                    break
            if dead:
                break


        #Draw everything
        pygame.draw.rect(win, (0,0,0), pygame.Rect(0,0,width,height)) #black background
        removes = []
        for i in tankList:
            if i.update(win):
                removes.append(i) #It was stuttering when I removed here but this works so yeah
        for i in removes:
            deadTanks.append(i)
            tankList.remove(i)
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
        #Side bar
        pygame.draw.rect(win, (200,200,200), pygame.Rect(width,0,width+200,height))
        counter = 50
        name = font.render('Name', True, (255,0,0))
        loc = name.get_rect()
        loc.right = width+75
        loc.bottom = counter-10
        win.blit(name, loc)
        kills = font.render('Kills', True, (255,0,0))
        loc = kills.get_rect()
        loc.left = width+100
        loc.bottom = counter-10
        win.blit(kills, loc)
        topKillList = []
        for i in tankList:
            topKillList.append([i.name, i.kills, False])
        for i in deadTanks:
            topKillList.append([i.name, i.kills, True]) #True for dead, False for not dead
        topKillList.sort(key = lambda x: x[1])
        topKillList.reverse()
        for i in topKillList:
            if i[2]:
                text = font.render(i[0], True, (255,100,100))
            else:
                text = font.render(i[0], True, (0,0,0))
            loc = text.get_rect()
            loc.right = width+75
            loc.top = counter
            win.blit(text, loc)
            text = font.render(str(i[1]), True, (0,0,0))
            loc = text.get_rect()
            loc.left = width+115
            loc.top = counter
            win.blit(text, loc)
            counter += 25
        pygame.display.update()

class playerUpdates:
    #Return 'right', 'left', 'sright', or 'sleft' | 'forward' or 'backward' | True or False
    #You CAN return nothing for the first two, but must return True or False for the last part
    def Rando(loc, dir, move, angle, bullets, info):
        lr = ['left', 'right', '', ''] #2 blanks for chance to not change direction
        fb = ['forward', 'backward', '']
        if randint(0,20) == 1:
            return lr[randint(0,3)], fb[randint(0,2)], True
        else:
            return dir, move, True
    def Chris(loc, dir, move, angle, bullets, info):
        selfShots = []
        for i in info:
            if not(i[0] == loc):
                pass
            else:
                selfShots = i[2]
        def dist(p1, p2):
            return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
        def safe(pos):
            if not(0+tankHeight < pos[0] < width-tankHeight):
                return False, ''
            if not(0+tankHeight < pos[1] < height-tankHeight):
                return False, ''
            for i in info:
                if not(i[0] == pos):
                    for x in i[2]:
                        for val in range(10,1000, 20):
                            newX = x.x+cos(radians(x.angle))*val
                            newY = x.y-sin(radians(x.angle))*val
                            if pos[0]-tankHeight/2 < newX < pos[0]+tankHeight/2 and loc[1]-tankHeight/2 < newY < loc[1]+tankHeight/2:
                                return False, x
                        #pygame.draw.line(win, (255,255,255), (x.x, x.y), (x.x+cos(radians(x.angle))*val, x.y-sin(radians(x.angle))*val))
            return True, ''
        temp, shot = safe(loc)
        if temp: #if safe
            #find closest tank
            closest = [-1000,-1000]
            for i in info:
                if not(i[0] == loc):
                    if dist(loc, i[0]) < dist(loc, closest):
                        closest = i[0]
            #turn to closest tank
            ang = atan2(closest[1]-loc[1], closest[0]-loc[0])
            ang = ang*180/pi
            if angle > 180:
                compareAngle = 360-angle
            else:
                compareAngle = -angle
            shoot = False
            dir2 = ''
            if abs(compareAngle - ang) < 2 and (bullets >= 3 or len(selfShots) >= 1):
                shoot = True
            elif abs(compareAngle-ang) < 2 and dist(loc,closest) < 50:
                shoot = True
            if abs(compareAngle - ang) < 20 and (bullets >= 3 or len(selfShots) >= 1):
                if dist(loc, closest) > 50:
                    dir2 = 'forward'
            dir1 = ''
            if compareAngle < ang:
                dir1 = 'right'
            if compareAngle > ang:
                dir1 = 'left'
            if abs(compareAngle-ang) < 10:
                if compareAngle < ang:
                    dir1 = 'sright'
                if compareAngle > ang:
                    dir1 = 'sleft'
            return dir1, dir2, shoot
        else:
            dir1 = dir
            dir2 = move
            newAngle = angle
            startAngle = 0
            for i in range(startAngle,startAngle+360,10):
                #pygame.draw.circle(win, (255,255,255), (int(loc[0]+cos(radians(i))*40), int(loc[1]+sin(radians(i))*40)), 2, 2)
                temp, empty = safe([loc[0]+cos(radians(i))*20, loc[1]+sin(radians(i))*20])
                if temp:
                    newAngle = i
                    break
            if angle < newAngle:
                dir1 = 'left'
            elif angle > newAngle:
                dir1 = 'right'
            try: #There is an error when the other tank dies i think so this just ignores that
                if abs(shot.angle - angle) < 180:
                    dir2 = 'forward'
                else:
                    dir2 = 'backward'
                    if dir1 == 'left':
                        dir1 = 'right'
                    else:
                        dir1 == 'right'
            except:
                pass
            return dir1, dir2, False
        return 'left', 'forward', False
    def Keys(loc, dir, move, angle, bullets, info):
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
        if keys[pygame.K_SPACE]:
            return dir2, dir1, True
        else:
            return dir2, dir1, False

end = True
while end:
    main()
