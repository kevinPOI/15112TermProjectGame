from PIL import Image
from PIL import ImageTk
from cmu_112_graphics import *
import math
from test1 import *
import time

#im1.show()


def appStarted(app):
    (app.width, app.height) = (960, 640)
    fFrame0 = Image.open("Characters/45F0.png")
    fFrame1 = Image.open("Characters/45F1.png")
    fFrame2 = Image.open("Characters/45F2.png")
    fFrame3 = Image.open("Characters/45F3.png")
    fFrame4 = Image.open("Characters/45F4.png")
    app.charF = [fFrame0, fFrame1, fFrame2, fFrame3, fFrame4]
    app.charR = []
    app.charI = []
    app.charStatus = 'idle'
    app.charHeadingLeft = False
    app.charX, app.charY = app.width/2, app.height/2
    app.dx, app.dy = 0, 0
    app.recoil = 0
    for i in range(0, 13): #load running chibi
        app.charR.append(Image.open(f"Characters/45R{i}.png"))
    for i in range(0, 11): #load idling chibi
        app.charI.append(Image.open(f"Characters/45I{i}.png"))
    for i in range(0, len(app.charF)):#resize firing chibi
        app.charF[i] = app.charF[i].resize((100,140))
    for i in range(0, len(app.charR)):#resize running chibi
        app.charR[i] = app.charR[i].resize((100,140))
    for i in range(0, len(app.charI)):#resize idling chibi
        app.charI[i] = app.charI[i].resize((100,140))
    app.background = Image.open("background.png")
    app.background = app.background.resize((960, 640))
    app.crosshairX, app.crosshairY = 0,0
    app.pointerF, app.pointerR, app.pointerI = 0, 0, 0
    app.idleAdd = False 
    app.bullets = []
    app.tickCount = 0
    app.fireAng = 0
    app.frameCount = 0
    app.frameCountFive = 0
    app.startTime = time.time()
    app.lastFrameTime = time.time()
def timerFired(app):
    app.pointerF += 1
    app.pointerR += 1
    if app.idleAdd == True:#idling is 1 frame per two ticks
        app.pointerI += 1
        app.idleAdd = False
    else:
        app.idleAdd = True
    if app.pointerF == len(app.charF):
        app.pointerF = 0
    if app.pointerR == len(app.charR):
        app.pointerR = 0
    if app.pointerI == len(app.charI):
        app.pointerI = 0
    app.charX += app.dx
    app.charY += app.dy
    if app.dx != 0 or app.dy != 0:
        app.charStatus = 'run'
    else:
        if app.charStatus != 'fire':
            app.charStatus = 'idle'
    if app.tickCount == 0:
        if app.charStatus == 'fire':
            app.bullets.append([app.charX, app.charY,app.fireAng,app.charHeadingLeft])
            app.tickCount =3
    else:
        if app.tickCount > 0:
            app.tickCount -=1
                
    i = 0
    while i < len(app.bullets):
        if app.bullets[i][0] > app.width:
            app.bullets.pop(i)
        else:
            if app.bullets[i][3]:
                app.bullets[i][0] -= 45 * math.cos(app.bullets[i][2])
                app.bullets[i][1] -= 45* math.sin(app.bullets[i][2])
            else:
                app.bullets[i][0] += 45 * math.cos(app.bullets[i][2])
                app.bullets[i][1] += 45* math.sin(app.bullets[i][2])
            i += 1
    
def mousePressed(app, event):
    if event.x - app.charX == 0:
        app.fireAng = 0.5
    else:
        app.fireAng = math.atan((event.y - app.charY)/(event.x - app.charX))
    if abs(app.fireAng)<0.25:
        if app.charStatus != 'run':
            if event.x < app.charX:
                app.charHeadingLeft = True
            if event.x > app.charX:
                app.charHeadingLeft = False
            app.charStatus = 'fire'
def mouseDragged(app, event):
    if event.x - app.charX == 0:
        app.fireAng = 0.5
    else:
        app.fireAng = math.atan((event.y - app.charY)/(event.x - app.charX))
    if abs(app.fireAng)<0.25:
        if app.charStatus != 'run':
            if event.x < app.charX:
                app.charHeadingLeft = True
            if event.x > app.charX:
                app.charHeadingLeft = False
            app.charStatus = 'fire'
    else:
        app.charStatus = 'idle'
def mouseReleased(app, event):
    app.charStatus = 'idle'
def mouseMoved(app, event):
    if event.x - app.charX == 0:
        app.fireAng = 0.5
    else:
        app.fireAng = math.atan((event.y - app.charY)/(event.x - app.charX))
def keyPressed(app, event):
    if event.key == 'd':
        #app.charStatus = 'run'
        app.charHeadingLeft = False
        app.dx = 10
    if event.key == 'a':
        #app.charStatus = 'run'
        app.charHeadingLeft = True
        app.dx = -10
    if event.key == 's':
        #app.charStatus = 'run'
        app.dy = 10
    if event.key == 'w':
        #app.charStatus = 'run'
        app.dy = -10
def keyReleased(app,event):
    if event.key == 'd':
        #app.charStatus = 'idle'
        app.dx = 0
    if event.key == 'a':
        #app.charStatus = 'idle'
        app.dx = 0
    if event.key == 's':
        #app.charStatus = 'idle'
        app.dy = 0
    if event.key == 'w':
        #app.charStatus = 'idle'
        app.dy = 0
def drawChar(app, canvas):
    if app.charStatus == 'fire':
        if app.charHeadingLeft:
            leftChar = app.charF[app.pointerF].transpose(Image.FLIP_LEFT_RIGHT)
            im_tk = ImageTk.PhotoImage(leftChar)
        else:
            im_tk = ImageTk.PhotoImage(app.charF[app.pointerF])
    elif app.charStatus == 'run':
        if app.charHeadingLeft:
            leftChar = app.charR[app.pointerR].transpose(Image.FLIP_LEFT_RIGHT)
            im_tk = ImageTk.PhotoImage(leftChar)
        else:
            im_tk = ImageTk.PhotoImage(app.charR[app.pointerR])
    else:
        if app.charHeadingLeft:
            leftChar = app.charI[app.pointerI].transpose(Image.FLIP_LEFT_RIGHT)
            im_tk = ImageTk.PhotoImage(leftChar)
        else:
            im_tk = ImageTk.PhotoImage(app.charI[app.pointerI])
    #canvas.create_image(app.charX, app.charY, image = im_tk)
    canvas.create_image(app.width/2, app.charY, image = im_tk)
def drawBackground(app, canvas):
    background = ImageTk.PhotoImage(app.background)
    canvas.create_image(app.width/2 + (app.width/2 - app.charX), app.height/2, image = background)
    canvas.create_image(2 * app.width - app.charX, app.height/2, image = background)
def get_elapsed_time(app):
    if app.frameCountFive == 20:
        endTime = time.time()
        elapsedTime = endTime - app.lastFrameTime
        print(20 / elapsedTime)
        app.lastFrameTime = endTime
        app.frameCountFive = 0
    app.frameCountFive += 1
def redrawAll(app,canvas):
    #get_elapsed_time(app)
    drawBackground(app, canvas)
    #canvas.create_rectangle(0, 0, app.width, app.height, fill="grey")
    drawChar(app, canvas)
    #canvas.create_oval(app.crosshairX - 5,app.crosshairY - 5, app.crosshairX + 5, app.crosshairY + 5, fill="red")
    for bullet in app.bullets:
        canvas.create_line(bullet[0]-5, bullet[1], bullet[0]+5, bullet[1], fill='yellow')
    if abs(app.fireAng) > 0.25:
        canvas.create_rectangle(app.width/2 - 100, app.height - 100, app.width/2 + 100, app.height -150, fill="red")
    else:
        canvas.create_rectangle(app.width/2 - 100, app.height - 100, app.width/2 + 100, app.height -150, fill="green")
def main():
    runApp(width = 960,height = 640)
    

if __name__ == '__main__':
    main()
    