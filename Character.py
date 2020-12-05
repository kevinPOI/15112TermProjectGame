from cmu_112_graphics import *
import math
from PhysicalObjects import *

import time
import random
def inDrawRange(y,app):
    if y > app.ff.cy - app.height / 2:
        if y < app.ff.cy + app.height / 2:
            return True
    return False
class Character(object):
    def __init__(self):
        self.charStatus, self.charHeadingLeft = 'idle', False
        self.pointerF = self.pointerR = self.pointerI = 0
        self.charF, self.charR, self.charI = [], [], []
        self.cx, self.cy, self.dx, self.dy = 480, 50, 0, 0
        self.tickCount = 0
        self.onGround = False
        self.loadResources()
        self.hp = 200
        self.isSliding = False
        self.ammoCount = 30
        self.outOfFiringArc = False
        self.standingOn = (0, 0)
    def loadResources(self):
        fFrame, rFrame, iFrame = 5, 13, 11
        self.charSize = (80,120)
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
        #if self.dx != 0 or self.dy != 0:
            #self.charStatus = 'run'
        #else:
        
        self.cx += self.dx
        self.cy += self.dy
    def fire(self, app, ang):
        if self.tickCount == 0 and self.ammoCount > 0:
            self.ammoCount -= 1
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
        canvas.create_text(app.width / 2, app.height * 0.95, 
        text = f"HP: {self.hp} / 100", font = "Arial 16 bold")
        if self.ammoCount <= 0:
            canvas.create_text(app.width * 0.5, app.height * 0.75,
            text = "Out Of Ammo", font = "Arial 24 bold", fill  = "red")
        elif self.outOfFiringArc:
            canvas.create_text(app.width * 0.5, app.height * 0.75,
            text = "Out Of Firing Arc", font = "Arial 24 bold", fill  = "red")
        canvas.create_text(app.width / 6, app.height * 0.95, 
        text = f"Ammo: {self.ammoCount}", font = "Arial 14 bold")
        if app.chaser.y < self.cy - app.height / 2:
            canvas.create_text(app.width * 0.5, app.height * 0.05,
            text = str(int(self.cy - app.chaser.y)) + "m", font = "Arial 20", fill  = "orange")
        canvas.create_text(app.width * 0.85, app.height * 0.05, text = "Score:"
        + str(int(self.cy)) + "m", font = "Arial 14 bold")