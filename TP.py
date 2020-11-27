#name: Kevin Tang
#andrewID: zhenrant
#images of characters from game http://gf.sunborngame.com/
#gifs extracted by: https://gfl.zzzzz.kr/doll.php?id=103&lang=en
#I screen captured them, converted them to frames, and have backgrounds removed
from PIL import Image
from PIL import ImageTk
from cmu_112_graphics import *
import math


import time
import random
class Platform(object):
    h = 10
    def __init__(self, x, y, r, ang):
        self.x = x
        self.y = y
        self.r = r
        self.ang = ang
        self.x0, self.x1 = x - r * math.cos(ang), x + r * math.cos(ang)
        self.y0, self.y1 = y - r * math.sin(ang), y + r * math.sin(ang)
        print(self.ang)
    def collisionY(self, cx, r):
        if self.ang > 0:
            cx -= r
        else:
            cx += r
        colY = self.y + (cx - self.x) * math.sin(self.ang)
        return colY
    def drawPlatform(self, app, canvas):
        canvas.create_line(self.x0, relativeY(app, self.y0),
         self.x1, relativeY(app, self.y1), width = self.h * 1.5)
class icePlatform(Platform):
    #__init__(self):
    pass
class Projectile(object):
    def __init__(self, x, y, ang):
        self.x = x
        self.y = y
        self.ang = ang
        self.remove = False
        self.hp = 3
    def move(self, app):
        self.x += self.dx
        self.y += self.dy
        self.dy += 2
        if self.x > app.width or self.x < 0:
            self.dx *= -1
        #self.reflect(app)
        if relativeY(app, self.y) > app.height * 1.5 or self.hp <= 0:
            self.remove = True
    def reflect(self, app):
        for platform in app.platforms:
            if ((self.x < platform.x0 and self.x + self.dx > platform.x0) or
            (self.x > platform.x1 and self.x + self.dx < platform.x1)):
                print("x test pass")
                if platform.ang > 0:
                    if ((self.y < platform.y0 and self.y + self.dy > platform.y0) or
                    (self.y > platform.y1 and self.y + self.dy < platform.y1)):
                        #self.dx *= math.cos(platform.ang)
                        self.dy *= - math.cos(platform.ang)
                        self.hp -= 1
                        print("colpos")
                else:
                    if ((self.y < platform.y1 and self.y + self.dy > platform.y1) or
                    (self.y > platform.y0 and self.y + self.dy < platform.y0)):
                        #self.dx *= math.cos(platform.ang)
                        self.dy *= - math.cos(platform.ang)
                        self.hp -= 1
                        print("colneg")
class Bullet(Projectile):
    def __init__(self, x, y, ang):
        super().__init__(x, y, ang)
        self.r = 5
        v = 50
        self.dx = v * math.cos(self.ang)
        self.dy = v * math.sin(self.ang)
    def drawBullet(self, app, canvas):
        canvas.create_rectangle(self.x -self.r, relativeY(app, self.y) - 1, 
        self.x + self.r, relativeY(app, self.y) + 1)
class Enemy(object):
    def __init__(self, x, y):
        self.hp = 50
        self.x = x
        self.y = y
        self.r = 40
        self.remove = False
    def drawEnemy(self, app, canvas):
        canvas.create_rectangle(0, relativeY(app, self.y) + 2,
         app.width, relativeY(app, self.y) - 2, fill = 'red')
        canvas.create_oval(self.x - self.r,
        relativeY(app, self.y) - self.r, self.x + self.r,
        relativeY(app, self.y) + self.r, fill = 'grey')
        
    def checkCollide(self, app):
        i = 0
        while i < len(app.projectiles):
            if app.projectiles[i].x > self.x - self.r:
                if app.projectiles[i]. x < self.x + self.r:
                    if app.projectiles[i].y > self.y - self.r:
                        if app.projectiles[i].y < self.y + self.r:
                            self.hp -= 10
                            app.projectiles.pop(i)
                            i -= 1
            i += 1
        if self.hp <= 0:
            self.remove = True
        if not self.remove and self.y < app.ff.cy + 50:
            app.ff.hp -= 50
            self.remove = True
            if app.ff.hp <= 0:
                app.gameOver = True
class Character(object):
    def __init__(self):
        self.charStatus, self.charHeadingLeft = 'idle', False
        self.pointerF = self.pointerR = self.pointerI = 0
        self.charF, self.charR, self.charI = [], [], []
        self.cx, self.cy, self.dx, self.dy = 360, 0, 0, 0
        self.tickCount = 0
        self.onGround = False
        self.loadResources()
        self.hp = 100
    def loadResources(self):
        fFrame, rFrame, iFrame = 5, 13, 11
        self.charSize = (90,130)
        for i in range (0, fFrame):
            self.charF.append(Image.open(f"Characters/45F{i}.png"))
            self.charF[i] = self.charF[i].resize(self.charSize)
        for i in range (0, rFrame):
            self.charR.append(Image.open(f"Characters/45R{i}.png"))
            self.charR[i] = self.charR[i].resize(self.charSize)
        for i in range (0, iFrame):
            self.charI.append(Image.open(f"Characters/45I{i}.png"))
            self.charI[i] = self.charI[i].resize(self.charSize)     
    def move(self):
        if self.dx != 0 or self.dy != 0:
            self.charStatus = 'run'
        else:
            if self.charStatus != 'fire':
                self.charStatus = 'idle'
        self.cx += self.dx
        self.cy += self.dy
    def fire(self, app, ang):
        if self.tickCount == 0:
            if self.charHeadingLeft:
                app.projectiles.append(Bullet(self.cx, self.cy, math.pi + ang))
            else:
                app.projectiles.append(Bullet(self.cx, self.cy, ang))
        self.tickCount += 1
        if self.tickCount > 6:#rof control (7 frames per shot)
            self.tickCount = 0
    def drawChar(self, app, canvas):
        if app.ff.charStatus == 'fire':
            if app.ff.charHeadingLeft:
                leftChar = app.ff.charF[app.ff.pointerF].transpose(Image.FLIP_LEFT_RIGHT)
                im_tk = ImageTk.PhotoImage(leftChar)
            else:
                im_tk = ImageTk.PhotoImage(app.ff.charF[app.ff.pointerF])
        elif app.ff.charStatus == 'run':
            if app.ff.charHeadingLeft:
                leftChar = app.ff.charR[app.ff.pointerR].transpose(Image.FLIP_LEFT_RIGHT)
                im_tk = ImageTk.PhotoImage(leftChar)
            else:
                im_tk = ImageTk.PhotoImage(app.ff.charR[app.ff.pointerR])
        else:
            if app.ff.charHeadingLeft:
                leftChar = app.ff.charI[app.ff.pointerI].transpose(Image.FLIP_LEFT_RIGHT)
                im_tk = ImageTk.PhotoImage(leftChar)
            else:
                im_tk = ImageTk.PhotoImage(app.ff.charI[app.ff.pointerI])
        canvas.create_image(app.ff.cx, app.height/2, image = im_tk)
    def nextCharFrame(self):#update pointers pointing to the next frame of char
        fFrame, rFrame, iFrame = 5, 13, 11
        self.pointerF += 1
        if self.pointerR % 2 == 0:
            self.pointerI += 1
        self.pointerR += 1
        if self.pointerF >= fFrame:
            self.pointerF = 0
        if self.pointerI >= iFrame:
            self.pointerI = 0
        if self.pointerR >= rFrame:
            self.pointerR = 0
    def drawStats(self, app, canvas):
        canvas.create_text(app.width / 2, app.height * 0.9, 
        text = f"HP: {self.hp} / 100", font = "Arial 16 bold")
def createPlatforms(app):#autogenerate platforms
    app.platforms = []
    for i in range (0, 30):
        deltaX = random.randint(-300,300)
        deltaY = random.randint(-30, 30)
        deltaR = random.randint(-20,20)
        deltaAng = random.randint(-25, 25)
        deltaAng2 = random.randint(-25, 25)
        deltaAng *= deltaAng2
        deltaAng /= 1000
        print(deltaAng)
        app.platforms.append(Platform(app.width / 2 + deltaX, 
        100 * i + deltaY, 80 + deltaR, deltaAng))
def createEnemies(app):#autogenerate enemies
    app.enemies = []
    for i in range (0, 10):
        deltaX = random.randint(-300,300)
        deltaY = random.randint(-30, 30)
        app.enemies.append(Enemy(app.width / 2 + deltaX, 
        500 + i * 300 + deltaY))
def removeEnemies(app):#remove dead enemies
    i = 0
    while i < len(app.enemies):#check if enemies are dead
        if app.enemies[i].remove == True:
            app.enemies.pop(i)
        else:
            i += 1
def drawPlatforms(app, canvas):
    for platform in app.platforms:
        platform.drawPlatform(app, canvas)
def drawProjectiles(app, canvas):
    for projectile in app.projectiles:
        projectile.drawBullet(app, canvas)
def drawEnemies(app, canvas):
    for enemy in app.enemies:
        enemy.drawEnemy(app, canvas)
##################################################
def appStarted(app):
    app.ff = Character()
    (app.width, app.height) = (960, 720)
    createPlatforms(app)
    createEnemies(app)
    app.projectiles = []
    app.mouseAng = 0
    app.gameOver = False
#####################################################
def collide(char, platforms):#if char stands on platforms
    charH, charW = char.charSize
    for platform in platforms:
        if char.cx + charW / 4 > platform.x0:
            if char.cx - charW / 4 < platform.x1:
                if char.cy + charH / 2 > platform.collisionY(char.cx, charW/4) - platform.h * 1.5:
                    if char.cy + charH / 2 < platform.collisionY(char.cx, charW/4) + platform.h:
                        char.cy = platform.collisionY(char.cx, charW/4) - charH / 2
                        return True
    return False
    '''
def collide2(char, platforms):#if char stands on platforms
    charH, charW = char.charSize
    for platform in platforms:
        if char.cy + charH / 2 > platform.y - platform.h * 1.5:
            if char.cy + charH / 2 < platform.y + platform.h:
                if char.cx + charW / 4 > platform.x - platform.r:
                    if char.cx - charW / 4 < platform.x + platform.r:
                        print(char.cy, platform.collisionY(char.cx, charW / 4))
                        return True
    return False
    '''
def moveProjectiles(app):#update velocity and position of projectiles
    i = 0
    while i < len(app.projectiles):
        app.projectiles[i].move(app)
        if app.projectiles[i].remove == True:
            app.projectiles.pop(i)
            print("proj left:", len(app.projectiles))
        else:
            i += 1
def relativeY(app, y):#convert y for drawing
    diff = y - app.ff.cy  
    return app.height / 2 + diff
def timerFired(app):
    app.ff.nextCharFrame()
    app.ff.move()
    if not collide(app.ff, app.platforms):#gravity for character
        app.ff.dy += 2
        app.ff.onGround = False
        if app.ff.dy > 18:#terminal velocity
            app.ff.dy = 18
    else:
        app.ff.dy = 0
        app.ff.onGround = True
    if app.ff.charStatus == 'fire':
        app.ff.fire(app, app.mouseAng)
    moveProjectiles(app)
    for enemy in app.enemies:#check if enemies are hit by projectile
        enemy.checkCollide(app)
    removeEnemies(app)
def keyPressed(app, event):
    if event.key == 'd':
        app.ff.charHeadingLeft = False
        app.ff.dx = 10
    if event.key == 'a':
        app.ff.charHeadingLeft = True
        app.ff.dx = -10
    if event.key == 's':
        app.ff.dy = 10
    if event.key == 'w':
        if app.ff.onGround == True:
            app.ff.dy = -20
def keyReleased(app,event):
    if event.key == 'd':
        app.ff.dx = 0
    if event.key == 'a':
        app.ff.dx = 0
    if event.key == 's':
        app.ff.dy = 0
def mousePressed(app, event):#fire and change direction accordingly
    if event.x - app.ff.cx == 0:
        ang = 0.05
    else:
        ang = math.atan((event.y - app.height / 2)/(event.x - app.ff.cx))
    if abs(ang)<1:
        if app.ff.charStatus != 'run':
            if event.x < app.ff.cx:
                app.ff.charHeadingLeft = True
            if event.x > app.ff.cx:
                app.ff.charHeadingLeft = False
            app.ff.charStatus = 'fire'
            app.mouseAng = ang
def mouseDragged(app, event):#fire and change direction accordingly
    if event.x - app.ff.cx == 0:
        ang = 0.5
    else:
        ang = math.atan((event.y - app.height / 2)/(event.x - app.ff.cx))
    if abs(ang)<1:
        if app.ff.charStatus != 'run':
            if event.x < app.ff.cx:
                app.ff.charHeadingLeft = True
            if event.x > app.ff.cx:
                app.ff.charHeadingLeft = False
            app.ff.charStatus = 'fire'
            app.mouseAng = ang
def mouseReleased(app, event):#stop firing
    app.ff.charStatus = 'idle'
    app.ff.tickCount = 0
def redrawAll(app, canvas):
    app.ff.drawChar(app, canvas)
    app.ff.drawStats(app, canvas)
    drawPlatforms(app, canvas)
    drawProjectiles(app, canvas)
    drawEnemies(app, canvas)
    if app.gameOver:
        canvas.create_text(app.width / 2, app.height / 2, text = "game over",
        font = 'Arial 30 bold')
def main():
    runApp(width = 960, height = 720)

if __name__ == '__main__':
    main()
