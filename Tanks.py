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
    players = ['Rando', 'Connor', 'Jordan', 'Chris', 'Luke', 'Schuh', 'Matthew', 'Michael', 'Ben', 'Chapin', 'Allen']
    shuffle(players)
    counter = len(players)
    for i in range(0,counter):
        for x in range(1,1): #Number of repeated tanks
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
    def Luke(loc, dir, move, angle, bullets, info):
        def bestMove(x1, x2, y1, y2, angle, shotAngle, shot):  # Calculates the best move
            # Calculates new position of bullet
            if shot == True:
                x2 += cos(radians(shotAngle)) * shotSpeed
                y2 -= sin(radians(shotAngle)) * shotSpeed

            # Calculates new position of tank
            distance = 0
            dirF = 0
            moveF = 0
            for d in range(1, 3):
                dir = d
                for m in range(1, 3):
                    move = m
                    if dir == 1:  # Left
                        angle += turnSpeed
                        if angle > 360:
                            angle -= 360
                    if dir == 2:  # Right
                        angle -= turnSpeed
                        if angle < 0:
                            angle += 360
                    if move == 1:  # Forward
                        if 0 + tankHeight / 2 < x1 + cos(radians(
                                angle)) * moveSpeed < width - tankHeight / 2:
                            x1 += cos(radians(angle)) * moveSpeed
                        if 0 + tankHeight / 2 < y1 - sin(radians(angle)) * moveSpeed < height - tankHeight / 2:
                            y1 -= sin(radians(angle)) * moveSpeed
                    if move == 2:  # Backward
                        if 0 + tankHeight / 2 < x1 - cos(radians(angle)) * moveSpeed < width - tankHeight / 2:
                            x1 -= cos(radians(angle)) * moveSpeed
                        if 0 + tankHeight / 2 < y1 + sin(radians(angle)) * moveSpeed < height - tankHeight / 2:
                            y1 += sin(radians(angle)) * moveSpeed
                    temp = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    if temp > distance:
                        distance = temp
                        dirF = dir
                        moveF = move
            if dirF == 1:
                dirF = 'left'
            if dirF == 2:
                dirF = 'right'
            if moveF == 1:
                moveF = 'forward'
            if moveF == 2:
                moveF = 'backward'
            return dirF, moveF

        def safe():  # Calculates if a bullet is going to hit
            for i in info:
                if not (i[0] == loc):
                    shots = i[2]
                    for a in shots:
                        if abs(a.x - loc[0]) < tankHeight * 3 and abs(a.y - loc[1]) < tankHeight * 3:
                            pass #"Not Safe")
                            return False, a.angle, a.x, a.y

            return True, 0, 0, 0

        shoot = False
        move = 'forward'
        shot = True
        safe, shotAngle, shotX, shotY = safe()

        # Calculates attack angle of closest tank
        if len(info) > 1:
            distance = 999
            x1 = loc[0]
            y1 = loc[1]
            attack = 0
            for i in range(len(info)):  # Inputs the closest tank position
                if info[i][0][0] != loc[0]:
                    x2 = info[i][0][0]
                    y2 = info[i][0][1]
                    temp = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    if temp < distance:
                        distance = temp
                        attack = i
            x2 = info[attack][0][0]
            y2 = info[attack][0][1]
            deltax = x2 - x1
            deltay = y2 - y1
            angle_rad = atan2(deltay, deltax)
            attackAngle = angle_rad * 180.0 / pi
            if attackAngle < 0:
                attackAngle = attackAngle + 360
            attackAngle = 360 - attackAngle

            # Avoiding other tanks
            if sqrt(deltax ** 2 + deltay ** 2) < 100:
                shot = False
                safe = False

        if len(info) > 1 and safe:  # Safe and there is more than 1 tank left
            # Calculates when to shoot
            dist = sqrt(deltax ** 2 + deltay ** 2)
            spray = ''
            if (dist < 200 and (attackAngle - 5 <= angle <= attackAngle + 5)) or bullets >= 3:
                shoot = True

            # Calculates where to move
            if dist < 100:
                move = ''
            angleDif = degrees(
                atan2(sin(radians(attackAngle) - radians(angle)), cos(radians(attackAngle) - radians(angle))))
            if angleDif < 0:
                return 'right', move, shoot
            else:
                return 'left', move, shoot

        else:  # Not Safe
            if shot == True:
                dirF, moveF = bestMove(loc[0], shotX, loc[1], shotY, angle, shotAngle, shot)
            if shot == False:  # Avoiding other tanks
                dirF, moveF = bestMove(loc[0], x2, loc[1], y2, angle, 0, shot)
            return dirF, moveF, shoot
    def Schuh(loc, dir, move, angle, bullets, info):

        for i in info:
            if(i[0]==loc):
                pass
            else:
                posi = xy=i[0]

        left_right = ['left', 'right'] #2 blanks for chance to not change direction
        front_back = ['forward', 'backward']
        
        if randint(0,20) == 1:
            return left_right[randint(0,1)], front_back[randint(0,1)], True
        else:
            return dir, move, True
    def Matthew(loc, dir, move, angle, bullets, info):
        x=0
        xpos=0
        ypos=0
        dir=''
        shoot=False
        turn=''

        shotslist=[]
        for i in info:
            for shots in i[2]:
                if(shots.x!=loc[0]):
                    shotslist.append(shots)

        enemypositions=[]
        for i in info:
            if(i[0][0]!=loc[0]):
                enemypositions.append(i[0])

        bulletX=loc[0]
        bulletY=loc[1]
        bulletlocs=[]
        while(bulletX>= -10 and bulletX<=width+10 and bulletY>= -10 and bulletY<=height+10):
            bulletX+=cos(radians(angle))*shotSpeed
            bulletY-=sin(radians(angle))*shotSpeed
            bulletlocs.append([bulletX,bulletY])


        if(bullets>0):
            for pos in enemypositions:
                bulletX=loc[0]
                bulletY=loc[1]
                bulletlocs=[]
                while(bulletX>= -10 and bulletX<=width+10 and bulletY>= -10 and bulletY<=height+10):
                    bulletX+=cos(radians(angle))*shotSpeed
                    bulletY-=sin(radians(angle))*shotSpeed
                    bulletlocs.append([bulletX,bulletY])
                    if abs(bulletX-pos[0])<tankHeight/2 and abs(bulletY-pos[1])<tankHeight/2:
                        shoot=True

        if(len(shotslist)==0) and bullets==0:
            dir='forward'

        rand=randint(1,20)
        if(rand==7):
            turn='right'
        else:
            turn='sright'

        rand=randint(1,8)
        if(rand==1):
            dir='forward'

        for shot in shotslist:
            shotX=shot.x
            shotY=shot.y
            shotA=shot.angle
            while(shotX >= -10 and shotX<=width+10 and shotY>= -10 and shotY<=height+10):
                shotX+=cos(radians(shotA))*shotSpeed
                shotY-=sin(radians(shotA))*shotSpeed
                if abs(shotX-loc[0])<tankHeight/2 and abs(shotY-loc[1])<tankHeight/2:
                    if(angle==shotA or 170<abs(angle-shotA)<190):
                        turn='left'
                    dir='backward'

        if (loc[0]<20 and loc[1]<20) or (loc[0]<20 and loc[1]>(height-20)) or (loc[0]>width-20 and loc[1]<20) or (loc[0]>width-20 and loc[1]>height-20):
            dir='forward'
        elif(loc[0]<5 or loc[1]<5 or loc[0]>width-5 or loc[1]>height-5):
            dir='forward'


        return turn,dir,shoot
    def Ben(loc, dir, move, angle, bullets, info):

        def onScreen(x, y):
            return 0 <= x <= width and 0 <= y <= height

        shotsPerDir = 1

        switchTime = 3 * shotsPerDir * 3
        chaseRange = 200

        shoot = False

        targets = []
        dodge = []
        me = 0

        for tank in info:
            x = tank[0][0]
            y = tank[0][1]

            if loc != [x, y]:
                if 0 < x < width and 0 < y < height:
                    targets.append(tank)

                for shot in tank[2]:
                    dodge.append(shot)
            else:
                me = tank

        myX, myY = loc[0], loc[1]
        closest = [10000, ["left", 369], False]

        if True:
            targetInfo = []

            centerX = width / 2
            centerY = height / 2

            centerXDist = myX - centerX
            centerYDist = myY - centerY

            move = "forward"
            centerDist = sqrt((centerXDist ** 2) + (centerYDist ** 2))

            for tank in targets:

                x, y, eangle = tank[0][0], tank[0][1], tank[1]

                if time.time() % switchTime >= (switchTime * (2 / 3)):
                    eangle = (eangle + 180) % 360

                xDist = myX - x
                yDist = myY - y

                dist = sqrt((xDist ** 2) + (yDist ** 2))

                angleTo = 360 - (((atan2(yDist, xDist) * 180) / pi) + 180)

                ticksTo = floor(dist / shotSpeed)
                ticksToList = [ticksTo]

                futX, futY, futXDist, futYDist, futDist = 0, 0, 0, 0, 0

                for i in range(0, 10):
                    futX, futY = x + cos(radians(eangle)) * ticksTo * moveSpeed, y - sin(
                        radians(eangle)) * ticksTo * moveSpeed

                    futXDist, futYDist = myX - futX, myY - futY

                    futDist = sqrt((futXDist ** 2) + (futYDist ** 2))

                    ticksTo = floor(futDist / shotSpeed)
                    ticksToList.append(ticksTo)

                total = 0

                for i in ticksToList:
                    total += i

                ticksTo = round((total / len(ticksToList)) * .95)

                futX, futY = x + cos(radians(eangle)) * ticksTo * moveSpeed, y - sin(
                    radians(eangle)) * ticksTo * moveSpeed

                futXDist, futYDist = myX - futX, myY - futY

                futAngleTo = 360 - (((atan2(futYDist, futXDist) * 180) / pi) + 180)

                if (switchTime * (1 / 3)) <= time.time() % switchTime <= (switchTime * (2 / 3)) \
                        or not onScreen(futX, futY):
                    futAngleTo = angleTo

                left = [0]
                right = [0]

                if angle - turnSpeed > futAngleTo:
                    right = angle - futAngleTo
                    left = (360 - angle) + futAngleTo
                elif angle + turnSpeed < futAngleTo:
                    left = futAngleTo - angle
                    right = (360 - futAngleTo) + angle

                turn = [[], []]

                if right < left:
                    turn = ["right", right]
                elif left < right:
                    turn = ["left", left]
                else:
                    turn = ["", 0]

                aim = False

                if abs(((angleTo + 180) % 360) - tank[1]) <= 10:
                    aim = True

                decisionInfo = [dist, turn, aim]
                targetInfo.append(decisionInfo)

            for target in targetInfo:
                dist = target[0]
                adif = target[1][1]
                aim = target[2]
                if aim and not closest[2] and closest[0] > 100:
                    closest = target
                elif dist < closest[0] and not closest[2]:
                    closest = target
                elif adif < closest[1][1] and not closest[2]:
                    closest = target
                # pass #closest)

            pass #"Dir1: ", dir, " - AngleTurn: ", closest[1][1])
            if not (abs(closest[1][1]) < turnSpeed):
                dir = closest[1][0]

            elif abs(closest[1][1]) < turnSpeed and True:
                dir = "s" + closest[1][0]
                pass #"Dir2: ", dir, " - CDir: ", closest[1][0])
                shoot = True

        danger = []

        for shot in dodge:
            sx, sy, sangle = shot.x, shot.y, shot.angle

            collide = []

            prediction = 50 - 3 * len(info)
            if prediction < 10:
                prediction = 10

            angleToS = (360 - (((atan2(myY - sy, myX - sx) * 180) / pi) + 180))

            for i in range(0, prediction):
                tsx = sx + (cos(radians(sangle)) * shotSpeed) * i
                tsy = sy - (sin(radians(sangle)) * shotSpeed) * i

                xDist, yDist = myX - tsx, myY - tsy

                dist = round(sqrt((xDist ** 2) + (yDist ** 2)))

                if dist <= tankHeight * 2:
                    collide = [i, True]
                    sx = tsx
                    sy = tsy
                    break

            left = [0]
            right = [0]

            sangle = (shot.angle + 90) % 360

            xDist = myX - (sx + (cos(radians(sangle)) * shotSpeed) * i)
            yDist = myY - (sy - (sin(radians(sangle)) * shotSpeed) * i)

            sangle = 360 - (((atan2(yDist, xDist) * 180) / pi) + 180)

            if angle - turnSpeed > sangle:
                right = angle - sangle
                left = (360 - angle) + sangle
            elif angle + turnSpeed < sangle:
                left = sangle - angle
                right = (360 - sangle) + angle

            right *= 3
            left *= 3

            turn = [[], []]

            if right < left:
                turn = ["right", right]
            elif left < right:
                turn = ["left", left]
            else:
                turn = ["", 0]

            if len(collide) > 0:
                danger.append([turn, collide])

        pygame.display.update()
        highestDanger = [["", 0], [1000, False]]

        for shot in danger:
            priority = shot[1][0]
            willKill = shot[1][1]

            if willKill and priority < highestDanger[1][0]:
                highestDanger = shot

            # if priority < 3:
            #     tankHeight = 0
            # else:
            #     tankHeight = tankImg.get_rect().size

        move = ""

        # pass #"Angle Dif: ", highestDanger[0][1])

        if not abs(highestDanger[0][1]) < turnSpeed:
            dir = highestDanger[0][0]
            pass #"Dir: ", dir)
            move = "backward"
        elif not abs(highestDanger[0][1]) < .5:
            dir = "s" + highestDanger[0][0]
            pass #"Dir: ", dir)
            pass
        elif len(info) > 2 and len(closest) > 0:
            if move != "backward" and closest[0] > chaseRange:
                move = "forward"
            elif closest[0] <= chaseRange * (3 / 4):
                move = "backward"

        myFutX, myFutY = 0, 0

        if not onScreen(myFutX, myFutY):
            if move == "backward":
                move = "forward"
            elif move == "forward":
                move = "backward"

        shoot = len(me[2]) < 2 and shoot

        return dir, move, shoot

        lr = ['left', 'right', '', '']
        fb = ['forward', 'backward', '']

        targets = []
        dodge = []
        me = 0
        myX, myY = loc[0], loc[1]

        for tank in info:
            x = tank[0][0]
            y = tank[0][1]

            if loc != [x, y]:
                targets.append(tank)

                for shot in tank[2]:
                    dodge.append(shot)
            else:
                me = tank

        myShots = me[2]

        for shot in myShots:
            x = shot.x
            y = shot.y

            if len(targets) > 0:
                t = targets[0]
                tx = t[0][0]
                ty = t[0][1]

                angleToT = 360 - (((atan2(y - ty, x - tx) * 180) / pi) + 180)
                dist = sqrt((y - loc[1]) ** 2 + (x - loc[0]) ** 2)

                if randint(0, 100) == 0:
                    shot.x += -shot.x + tx - 10
                    shot.y += -shot.y + ty - 10
                    shot.angle = 360 - (((atan2(y - ty, x - tx) * 180) / pi) + 180)

                if dist < tankHeight or True:
                    shot.angle = angleToT

                    # printCoord("Before: ", shot.x, shot.y)

                    # printCoord("After: ", shot.x, shot.y)

        for shot in dodge:
            sx, sy, sangle = shot.x, shot.y, shot.angle

            collide = []

            prediction = 50 - 3 * len(info)
            if prediction < 10:
                prediction = 10

            angleToS = (360 - (((atan2(myY - sy, myX - sx) * 180) / pi) + 180))

            for i in range(0, prediction):
                tsx = sx + (cos(radians(sangle)) * shotSpeed) * i
                tsy = sy - (sin(radians(sangle)) * shotSpeed) * i

                xDist, yDist = myX - tsx, myY - tsy

                dist = round(sqrt((xDist ** 2) + (yDist ** 2)))

                if dist <= tankHeight * 2:
                    collide = [i, True]
                    sx = tsx
                    sy = tsy
                    break

            left = [0]
            right = [0]

            sangle = (shot.angle + 90) % 360

            xDist = myX - (sx + (cos(radians(sangle)) * shotSpeed) * i)
            yDist = myY - (sy - (sin(radians(sangle)) * shotSpeed) * i)

            sangle = 360 - (((atan2(yDist, xDist) * 180) / pi) + 180)

            if angle - turnSpeed > sangle:
                right = angle - sangle
                left = (360 - angle) + sangle
            elif angle + turnSpeed < sangle:
                left = sangle - angle
                right = (360 - sangle) + angle

            right *= 3
            left *= 3

            turn = [[], []]

            if right < left:
                turn = ["right", right]
            elif left < right:
                turn = ["left", left]
            else:
                turn = ["", 0]

            if len(collide) > 0:
                shot.x = -1000
                shot.y = -1000

        if randint(0, 20) == 1:
            return lr[randint(0, 3)], move, randint(0, 10) == 1
        elif randint(0, 20) == 1:
            return dir, fb[randint(0, 2)], randint(0, 10) == 1
        else:
            return dir, move, (randint(0, 20) == 1)


        me = []
        myShots = []

        tanks = []
        shots = []
        x, y = loc

        # Return info
        dir = ""
        move = "forward"
        shoot = False

        # Sorting [info] into [me], [myShots], [tanks], [shots]
        for tank in info:
            tankX, tankY = tank[0]

            if x == tankX and y == tankY:
                me = tank
                for shot in me[2]:
                    myShots.append(shot)
            else:
                tanks.append(tank)

                for shot in tank[2]:
                    shots.append(shot)

        # Closest tank
        cTank = [[-1000, -1000], 10, [], 0, 0]
        cTankDist = 10000
        # Determining the closest tank
        for tank in tanks:
            tankX, tankY = tank[0]

            xDist, yDist = x - tankX, y - tankY

            dist = sqrt((xDist ** 2) + (yDist ** 2))

            if dist < cTankDist:
                cTank = tank
                cTankDist = dist

        # If there are any tanks left, check my angle vs the angle to the
        # closest tank, and if the angles are similar, fire at that tank.
        if not cTank[0][0] == -1000:
            tankX, tankY = tank[0]

            xDist, yDist = x - tankX, y - tankY

            dist = sqrt((xDist ** 2) + (yDist ** 2))

            angleTo = 360 - (((atan2(y - tankY, x - tankX) * 180) / pi) + 180)

            if abs(angleTo - angle) < turnSpeed:
                pass #"Shoot")
                shoot = True
                dir = "sleft"
            else:
                dir = "left"
                shoot = False

        return dir, move, shoot
    def Jordan(loc, dir, move, angle, bullets, info):
        import math
        myPlayer = None
        myLocation = None
        allLocations = []
        closestPlayer = None
        distance = -1

        for player in info:
            if player == None:
                continue
            if player[0][0] < 0:
                continue
            if loc[0] == player[0][0] and loc[1] == player[0][1]:
                myPlayer = player
                myLocation = myPlayer[2]
                continue

            allLocations.append(player[2])

            if closestPlayer == None:
                closestPlayer = player
                distance = math.sqrt(math.pow(player[0][0] - loc[0], 2) + math.pow(
                    (player[0][1]) - loc[1], 2))
            else:
                distance = math.sqrt(math.pow((player[0][0]) - loc[0], 2) + math.pow(
                    (player[0][1]) - loc[1], 2))
                if distance < distance:
                    closestPlayer = player
                    distance = distance

        if (closestPlayer == None):
            return '', '', False

        rel_x, rel_y = (closestPlayer[0][0]) - loc[0], (closestPlayer[0][1]) - loc[1]
        lookAngle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        lookAngle = lookAngle % 360
        doThing = True

        if myLocation != None and doThing:
            for loc in myLocation:
                rel_x_bullet, rel_y_bullet = (closestPlayer[0][0]) - loc.x, (closestPlayer[0][1]) - loc.y
                lookAngleB = (180 / math.pi) * -math.atan2(rel_y, rel_x)
                lookAngleB = lookAngleB % 360
                if lookAngle > loc.angle:
                    test = lookAngle - loc.angle
                else:
                    test = loc.angle - lookAngle
                if test <= 76:
                    loc.angle = lookAngleB

        dir = ''
        moving = ''
        shoot = False

        test = 0

        if lookAngle > angle:
            test = lookAngle - angle
        else:
            test = angle - lookAngle

        if test <= 25:
            shoot = True

        if test >= 30:
            if lookAngle < angle:
                dir = 'right'
            if lookAngle > angle:
                dir = 'left'
        else:
            if lookAngle < angle:
                shoot = True
                dir = 'sright'
            if lookAngle > angle:
                shoot = True
                dir = 'sleft'
        if shoot:
            shoot = (len(myLocation) + bullets == 3 or bullets > 3)
        fb = ['forward', 'backward', '']
        return dir, fb[randint(0,2)], shoot
    def Chapin(loc,dir, move, angle, bullets, info):



        x=loc[0]
        y=loc[1]
        dir=""
        move=""
        bool=False
        targetnumber=0
        targetlocked=False

        if info[targetnumber][0]==loc:
            targetnumber+=1
            #pass #"targeted self")
        if len(info)==1:
            targetnumber=0

        targetx=info[targetnumber][0][0]
        targety=info[targetnumber][0][1]
        #print ("target:",targetx,targety)
        #pass #loc)
        #pass #angle)

        for i in range(len(info)):
            Ex, Ey = info[i][0][0], info[i][0][1]
            if [Ex, Ey] == [x, y]:
                    continue
            xdist = x - Ex
            ydist = y - Ey
            angleTo= floor(360 - (((atan2(ydist,xdist) * 180)/pi) +180))

            if abs(angle - angleTo) < turnSpeed:
                bool = True

        if (targetx-x)>5 and x<targetx:#if target it to the right and distance is greater than 5
            #pass #"target on right")
            if angle!=358 and angle!=359 and angle!=0 and angle!=1 and angle!=2:#if angle isn't perfect turn right
                dir="right"
                move="forward"
            else:
                move="forward"
                if y<targety:#target is below me
                    pass #"SouthEast")
                    dir="right"
                    if abs(angle - angleTo) < turnSpeed:
                        dir=""
                if y>targety:#target is above me
                    pass #"NorthEast")
                    dir="left"
                    if abs(angle - angleTo) < turnSpeed:
                        dir=""
        elif (x-targetx)>5 and x>targetx:#if the target is to the left and distance is greater than 5
            #pass #"target on left")
            if angle!=178 and angle!=179 and angle!=180 and angle!=181 and angle!=182:#if angle isn't perfect turn left
                dir="left"
                move="forward"
            else:
                move="forward"
                if y<targety:#target is below me
                    pass #"SouthWest")
                    dir="left"
                    if abs(angle - angleTo) < turnSpeed:
                        dir=""
                if y>targety:#target is above me
                    pass #"NorthWest")
                    dir='right'
                    if abs(angle - angleTo) < turnSpeed:
                        dir=""

        if (x-targetx)<5 and (targetx-x)<5:#on same x level
            targetlocked=True
            #pass #"locked")

        if y<targety and targetlocked:#if the target is below me
            #pass #"target is below")
            if angle!=268 and angle!=269 and angle!=270 and angle!=271 and angle!=272:#if not facing down
                if angle>90 and angle<270:#if facing right
                    dir="left"
                else:
                    dir="right"
            else:
                bool=True
                move="forward"
                #pass #"found vertical")
        elif targetlocked:#if the target is above me
            #pass #"target is above")
            if angle!=88 and angle!=89 and angle!=90 and angle!=91 and angle!=92:#if not facing up
                if angle>90 and angle<270:#if facing right
                    dir="right"
                else:
                    dir="left"
            else:
                move="forward"
                #pass #"found vertical")



        if y<targety:#target is below me
            pass #"SouthWest")
            dir="left"
            if abs(angle - angleTo) < turnSpeed:
                dir=""
        if y>targety:#target is above me
            pass #"NorthWest")
            dir='right'
            if abs(angle - angleTo) < turnSpeed:
                dir=""

        if y<targety:#target is below me
            pass #"SouthWest")
            dir="left"
            if abs(angle - angleTo) < turnSpeed:
                dir=""
        if y>targety:#target is above me
            pass #"NorthWest")
            dir='right'
            if abs(angle - angleTo) < turnSpeed:
                dir=""




        return (dir, move, bool)
    def Allen(loc, dir, move, angle, bullets, info):
        # Moves
        srr = ['right', 'sright']
        fb = ['']
        shoot = False
        shotx, shoty = loc
        myBulletPoints = []

        mex, mey = loc
        bulletPoints = []
        repeat = 0

        #Get enemy tanks and shots
        for tanks in info:
             if loc == tanks[0]:
                 info.pop(repeat)
             repeat += 1

        for tanks in info:
            for bullet in tanks[2]:
                bulletPoints.append([bullet.x, bullet.y])

                newbx = bullet.x
                newby = bullet.y
                while newbx >= -10 and newbx <= width + 10 and newby >= -10 and newby <= height + 10:
                    newbx = newbx + cos(radians(bullet.angle)) * shotSpeed
                    newby = newby - sin(radians(bullet.angle)) * shotSpeed
                    bulletPoints.append([newbx, newby])

        #Dodge enemy shots
        for bullet in bulletPoints:
            bulletx, bullety = bullet
            if abs(bulletx - mex) < tankHeight/2 and abs(bullety - mey) < tankHeight/2:
                return 'left', 'backward', shoot

        #Target enemies
        while shotx >= -10 and shotx <= width + 10 and shoty >= -10 and shoty <= height + 10:
            shotx += cos(radians(angle)) * shotSpeed
            shoty -= sin(radians(angle)) * shotSpeed
            myBulletPoints.append([shotx, shoty])

        for bullet in myBulletPoints:
            bulletx, bullety = bullet

            for tanks in info:
                ex, ey = tanks[0]
                random = randint(0, 4)
                if random == 0:
                    if abs(bulletx - ex) < tankHeight/2 and abs(bullety - ey) < tankHeight/2:
                        shoot = True
                else:
                    if abs(bulletx - ex) < tankHeight and abs(bullety - ey) < tankHeight:
                        shoot = True

        #Random turns
        if randint(0, 2) == 1:
            return srr[randint(0, 1)], fb[randint(0, 0)], shoot
        else:
            return dir, move, shoot
    def Michael(loc, dir, move, angle, bullets, info):
  
            shoot = False
            x, y = loc[0], loc[1]
            for i in info:
                ix, iy = i[0][0], i[0][1]
                cx, cy = x - ix, y - iy
                if cx != 0:
                    a = degrees(tan(cy / cx))
                    if abs(angle - a) <= 7:
                        if bullets > 0:
                            shoot = True
            return 'right', 'forward', shoot
    def Connor(loc, dir, move, angle, bullets, info):
        dir1, dir2, shoot = '', '', False
        x, y = loc[0], loc[1]
        target = 0
        TEx, TEy = info[target][0][0], info[target][0][1]
        try:
            if [TEx, TEy] == [x, y]:
                target += 1
                TEx, TEy = info[target][0][0], info[target][0][1]
        except IndexError:
            target = 0

        xdist = x - TEx
        ydist = y - TEy
        TangleTo = floor(360 - (((atan2(ydist, xdist) * 180) / pi) + 180))

        if abs(angle - TangleTo) <= 90:
            dir1 = 'forward'

        if abs(angle - TangleTo) > turnSpeed:
            if TangleTo >= 180:
                dir2 = 'right'
            elif TangleTo < 180:
                dir2 = 'left'

        for i in range(len(info)):
            Ex, Ey = info[i][0][0], info[i][0][1]
            if [Ex, Ey] == [x, y]:
                continue
            xdist = x - Ex
            ydist = y - Ey
            angleTo = floor(360 - (((atan2(ydist, xdist) * 180) / pi) + 180))

            if abs(angle - angleTo) < 8:
                shoot = True

        return dir2, dir1, shoot
end = True
while end:
    main()
