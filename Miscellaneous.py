
from PIL import Image
from PIL import ImageTk
from cmu_112_graphics_mod import *

from Character import *
from PhysicalObjects import *
import math


import time
import random


class Button(object):
    def __init__(self,x0,y0,x1,y1,text):
        self.x0, self.x1 = x0, x1
        self.y0, self.y1 = y0, y1
        self.text = text
    def clicked(self, x, y):
        if self.x0 < x < self.x1:
            if self.y0 < y < self.y1:
                return True
        return False
    def drawButton(self, canvas):
        x0, x1 = self.x0, self.x1
        y0, y1 = self.y0, self.y1
        canvas.create_rectangle(x0,y0,x1,y1,fill = "black")
        canvas.create_text((x1 + x0)/2, (y1 + y0)/2, text = self.text, font = "Aerial 18 bold", fill = 'yellow')
class Enhancement(object):
    def __init__(self,x0,y0,text):
        self.x0, self.y0 = x0, y0
        self.x1 = self.x0 + 140
        self.y1 = self.y0 + 100
        self.xMid = self.x0 + 70
        self.yDiv = self.y0 + 30
        self.text = text
        self.lv = 0
    def minusClicked(self, x, y,app):
        if self.x0 < x < self.xMid:
            if self.y0 < y < self.yDiv:
                if self.lv > 0:
                    self.lv -= 1
                    app.rp = app.hpE.lv +app.regenE.lv + app.dmgE.lv + app.ammoE.lv+app.grenadeE.lv
                return True
        return False
    def plusClicked(self, x, y,app):
        if self.xMid < x < self.x1:
            if self.y0 < y < self.yDiv:
                print(app.rp, app.bestScore)
                if self.lv < 3 and app.rp < int(app.bestScore / 600) and app.rp < 12:
                    self.lv += 1
                    app.rp = app.hpE.lv +app.regenE.lv + app.dmgE.lv + app.ammoE.lv+app.grenadeE.lv
                return True
    def drawEnhancement(self, canvas):
        x0, x1 = self.x0, self.x1
        y0, y1 = self.y0, self.y1
        canvas.create_rectangle(x0,y0,x1,y1,fill = "black")
        canvas.create_text(self.xMid, self.yDiv + 30, text = self.text + " lv:" + str(self.lv), font = "Calibri 14", fill = 'white')
        canvas.create_line(self.x0 + 15, self.yDiv - 15, self.x0 + 45, self.yDiv - 15, width = 5, fill = "yellow")
        canvas.create_line(self.xMid + 15, self.yDiv - 15, self.xMid + 45, self.yDiv - 15, width = 5, fill = "yellow")
        canvas.create_line(self.xMid + 30, self.yDiv - 3, self.xMid + 30, self.yDiv - 27,width = 5, fill = "yellow")
def drawChart(x, y, app, canvas):
    canvas.create_line(x, y + 400, x + 300, y + 400)
    canvas.create_line(x, y, x , y + 400)
    increment = 300 / len(app.charData)
    scale = 400 / max(app.charData)
    for i in range(0, len(app.charData) - 1):
        canvas.create_line(x + i * increment, y + 400- scale * app.charData[i], 
        x + (i + 1) * increment, y + 400 - scale * app.charData[i + 1], width = 2)
    for i in range(0, len(app.charData) - 1):
        canvas.create_line(x + i * increment, y + 400- scale * app.chaserData[i], 
        x + (i + 1) * increment, y + 400 - scale * app.chaserData[i + 1], fill = "red", width = 2)
    canvas.create_text(x + 350, y + 20, text = "character position")
    canvas.create_text(x + 350, y + 60, text = "deadline position", fill = "red")