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
    dx = 0
    dy = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 2
class Bullet(Projectile):
    dx = 30
    dy = 0
    r = 4
    def __init__(self, x, y):
        super().__init__(self, x, y)
    
    def drawBullet(self, canvas):
        canvas.create_rectangle(self.x -self.r, self.y - 1, self.x + self.r, self.y + 1)
class Character(object):
    def __init__(self):
        self.charStatus, self.charHeadingLeft = 'idle', False
        self.pointerF = self.pointerR = self.pointerI = 0
        self.charF, self.charR, self.charI = [], [], []
        self.cx, self.cy, self.dx, self.dy = 360, 0, 0, 0
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
    def fire(self, app):
        self.charStatus = 'fire'
        app.projectiles.append(bullet(self.cx, self.cy))
    def drawChar(self, app, canvas):
        if app.ff.charStatus == 'fire':
            if app.ff.charHeadingLeft:
                leftChar = app.ff.charF[app.ff.pointerF].transpose(Image.FLIP_LEFT_RIGHT)
                im_tk = ImageTk.PhotoImage(leftChar)
            else:
                im_tk = ImageTk.PhotoImage(app.ff.charF[app.pointerF])
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
    for i in range (0, 20):
        deltaX = random.randint(-300,300)
        deltaY = random.randint(-30, 30)
        deltaR = random.randint(-20,20)
        app.platforms.append(Platform(app.width / 2 + deltaX, 
        150 * i + deltaY, 80 + deltaR))

def drawPlatforms(app, canvas):
    for platform in app.platforms:
        platform.drawPlatform(app, canvas)
def appStarted(app):
    app.ff = Character()
    (app.width, app.height) = (960, 720)
    createPlatforms(app)
    app.projectiles = []
def collide(char, platforms):
    charH, charW = char.charSize
    for platform in platforms:
        if char.cy + charH / 2 > platform.y - platform.h * 1.5:
            if char.cy + charH / 2 < platform.y + platform.h:
                if char.cx + charW / 4 > platform.x - platform.r:
                    if char.cx - charW / 4 < platform.x + platform.r:
                        return True
    return False
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
def redrawAll(app, canvas):
    app.ff.drawChar(app, canvas)
    drawPlatforms(app, canvas)
def main():
    runApp(width = 960, height = 720)

if __name__ == '__main__':
    main()
