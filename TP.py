from PIL import Image
from PIL import ImageTk
from cmu_112_graphics import *
import math
import time
import random
class Platform(object):
    h = 10
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    def drawPlatform(self, app, canvas):
        canvas.create_rectangle(self.x - self.r, 
        relativeY(app, self.y) - self.h, self.x + self.r,
        relativeY(app, self.y) + self.h, fill = 'black')
class Projectile(object):
    def __init__(self, x, y, ang):
        self.x = x
        self.y = y
        self.ang = ang
        self.remove = False
    def move(self, app):
        self.x += self.dx
        self.y += self.dy
        self.dy += 2
        if self.x > app.width or self.x < 0:
            self.dx *= -1
        if relativeY(app, self.y) > app.height * 1.5:
            self.remove = True
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
        self.hp = 100
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
                    print("2pass")
                    if app.projectiles[i].y > self.y - self.r:
                        print("3pass")
                        if app.projectiles[i].y < self.y + self.r:
                            print("4pass")
                            self.hp -= 10
                            app.projectiles.pop(i)
                            i -= 1
            i += 1
        if self.hp <= 0:
            self.remove = True
        if not self.remove and self.y < app.ff.cy:
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
        if self.tickCount > 6:
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
        
    def nextCharFrame(self):
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
def createPlatforms(app):
    app.platforms = []
    for i in range (0, 30):
        deltaX = random.randint(-300,300)
        deltaY = random.randint(-30, 30)
        deltaR = random.randint(-20,20)
        app.platforms.append(Platform(app.width / 2 + deltaX, 
        100 * i + deltaY, 80 + deltaR))
def createEnemies(app):
    app.enemies = []
    for i in range (0, 10):
        deltaX = random.randint(-300,300)
        deltaY = random.randint(-30, 30)
        app.enemies.append(Enemy(app.width / 2 + deltaX, 
        500 + i * 300 + deltaY))
def removeEnemies(app):
    i = 0
    while i < len(app.enemies):
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
def collide(char, platforms):
    charH, charW = char.charSize
    for platform in platforms:
        if char.cy + charH / 2 > platform.y - platform.h * 1.5:
            if char.cy + charH / 2 < platform.y + platform.h:
                if char.cx + charW / 4 > platform.x - platform.r:
                    if char.cx - charW / 4 < platform.x + platform.r:
                        return True
    return False
def moveProjectiles(app):
    i = 0
    while i < len(app.projectiles):
        app.projectiles[i].move(app)
        if app.projectiles[i].remove == True:
            app.projectiles.pop(i)
        else:
            i += 1
def relativeY(app, y):
    diff = y - app.ff.cy  
    return app.height / 2 + diff
def timerFired(app):
    app.ff.nextCharFrame()
    app.ff.move()
    if not collide(app.ff, app.platforms):
        app.ff.dy += 2
        app.ff.onGround = False
        if app.ff.dy > 18:
            app.ff.dy = 18
    else:
        app.ff.dy = 0
        app.ff.onGround = True
    if app.ff.charStatus == 'fire':
        app.ff.fire(app, app.mouseAng)
    moveProjectiles(app)
    for enemy in app.enemies:
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
def mousePressed(app, event):
    if event.x - app.ff.cx == 0:
        ang = 0.5
    else:
        ang = math.atan((event.y - app.height / 2)/(event.x - app.ff.cx))
    if abs(ang)<0.7:
        if app.ff.charStatus != 'run':
            if event.x < app.ff.cx:
                app.ff.charHeadingLeft = True
            if event.x > app.ff.cx:
                app.ff.charHeadingLeft = False
            app.ff.charStatus = 'fire'
            app.mouseAng = ang
            print(ang)
def mouseDragged(app, event):
    if event.x - app.ff.cx == 0:
        ang = 0.5
    else:
        ang = math.atan((event.y - app.height / 2)/(event.x - app.ff.cx))
    if abs(ang)<0.7:
        if app.ff.charStatus != 'run':
            if event.x < app.ff.cx:
                app.ff.charHeadingLeft = True
            if event.x > app.ff.cx:
                app.ff.charHeadingLeft = False
            app.ff.charStatus = 'fire'
            app.mouseAng = ang
            print(ang)
def mouseReleased(app, event):
    app.ff.charStatus = 'idle'
    app.ff.tickCount = 0
def redrawAll(app, canvas):
    app.ff.drawChar(app, canvas)
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
