#name: Kevin Tang
#andrewID: zhenrant
#images of characters from game http://gf.sunborngame.com/
#gifs extracted by: https://gfl.zzzzz.kr/doll.php?id=103&lang=en
#I screen captured them, converted them to frames, and have backgrounds removed
from PIL import Image
from PIL import ImageTk
from cmu_112_graphics import *

from Character import *
from PhysicalObjects import *
import math


import time
import random

def inDrawRange(y,app):
    if y > app.ff.cy - app.height / 1.5:
        if y < app.ff.cy + app.height / 1.5:
            return True
    return False
def createPlatforms(app):#autogenerate platforms
    app.platforms = []
    app.walls = []
    for i in range (0, 45):
        deltaX = random.randint(-300,300)
        deltaY = random.randint(-30, 30)
        deltaR = random.randint(-20,20)
        deltaAng = random.randint(-25, 25)
        deltaAng2 = random.randint(-25, 25)
        deltaAng *= deltaAng2
        deltaAng /= 1000
        platformType = random.randint(0,3)
        if platformType == 3:
            app.platforms.append(IcePlatform(app.width / 2 + deltaX, 
            100 * i + deltaY, 80 + deltaR, deltaAng))
        else:
            app.platforms.append(Platform(app.width / 2 + deltaX, 
            100 * i + deltaY, 80 + deltaR, deltaAng))
        if platformType == 2:
            pass
def createEnemies(app):#autogenerate enemies
    app.enemies = []
    for i in range (0, 15):
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
def removeBots(app):#remove dead enemies
    i = 0
    while i < len(app.bots):#check if enemies are dead
        if app.bots[i].remove == True:
            app.bots.pop(i)
        else:
            i += 1
def generateMap(app, x, y):
    if y > 10000:
        terminate = False
        for platform in app.platforms:
            if abs(x - platform.x) < 200 and abs(y - platform.y) < 70:
                terminate = True
        if not terminate:
            app.platforms.append(Platform(app.width / 2, 
                200, 90, 0))
        
    else:
        terminate = False
        for platform in app.platforms:
            if abs(x - platform.x) < 200 and abs(y - platform.y) < 70:
                terminate = True
        if not terminate:
            deltaY = random.randint(-60, 60)
            deltaY2 = random.randint(-60, 60)
            deltaR = random.randint(-20,20)
            deltaAng = random.randint(-20, 20)
            deltaAng2 = random.randint(-20, 20)
            deltaAng *= deltaAng2
            deltaAng /= 1000
            platformType = random.randint(0,3)
            if platformType == 3:
                app.platforms.append(IcePlatform(x, 
                y, 60 + deltaR, deltaAng))
            else:
                app.platforms.append(Platform(x, 
                y, 60 + deltaR, deltaAng))
            maxDx = 2.2 * (((130 + deltaY) * 100) ** 0.5)
            maxDx2 = 2.2 * (((130 + deltaY) * 100) ** 0.5)
            generate = True
            for enemy in app.enemies:
                if y < 800 or abs(y - enemy.y) < 250:
                    generate = False
            if generate and random.randint(0,0) == 0:
                for platform in app.platforms:
                    if y + 50 - platform.y < 50:
                        generate = False
                if generate:
                    app.enemies.append(Enemy(x, y + 70))
                    pass
            if x + maxDx < app.width - 100:
                generateMap(app, x + maxDx, y + (130 + deltaY))
            if x - maxDx > 100:
                generateMap(app, x - maxDx2, y + (130 + deltaY2))
def createChaser(app):
    app.chaser = Chaser()
def drawPlatforms(app, canvas):
    for platform in app.platforms:
        if inDrawRange(platform.y, app):
            platform.drawPlatform(app, canvas)
def drawProjectiles(app, canvas):
    for projectile in app.projectiles:
        projectile.drawBullet(app, canvas)
def drawEnemies(app, canvas):
    for enemy in app.enemies:
        enemy.drawEnemy(app, canvas)
    for bot in app.bots:
        bot.drawEnemy(app, canvas)
##################################################
def appStarted(app):
    app.ff = Character()
    (app.width, app.height) = (960, 720)
    app.platforms = []
    app.enemies = []
    app.bots = []
    generateMap(app, app.width / 2, 300)
    print("num of plat:", len(app.platforms))
    #createEnemies(app)
    app.projectiles = []
    app.mouseAng = 0
    app.gameOver = False
    createChaser(app)
    app.bots.append(Bot(500, 800))
    app.bots.append(Bot(500, 1400))
    app.bots.append(Bot(500, 2000))
#####################################################
def standsOn(char, app):#if char stands on platforms
    charH, charW = char.charSize
    for platform in app.platforms:
        if inDrawRange(platform.y, app):
            if char.cx + charW / 4 > platform.x0:
                if char.cx - charW / 4 < platform.x1:
                    if char.cy + charH / 2 > platform.collisionY(char.cx, charW/4) - platform.h * 1.5:
                        if char.cy + charH / 2 < platform.collisionY(char.cx, charW/4) + platform.h:
                            if type(platform) == IcePlatform:
                                char.dx += 2 * math.tan(platform.ang)
                            char.cy = platform.collisionY(char.cx, charW/4) - charH / 2
                            char.standingOn = (platform.x, platform.y)
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
        else:
            i += 1
def relativeY(app, y):#convert y for drawing
    diff = y - app.ff.cy  
    return app.height / 2 + diff
def timerFired(app):
    if not app.gameOver:
        app.ff.nextCharFrame()
        app.ff.move()
        i = 0
        while i < len(app.bots):
            if app.bots[i].y < app.ff.cy + 500:
                app.bots[i].activated = True
            if app.bots[i].activated:
                app.bots[i].move(app)
            i += 1
        if not standsOn(app.ff, app):#gravity for character
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
        for bot in app.bots:
            bot.checkCollide(app)
        removeBots(app)
        removeEnemies(app)
        app.chaser.move(app)
def keyPressed(app, event):
    if event.key == 'd':
        app.ff.charHeadingLeft = False
        app.ff.dx = 10
        app.ff.charStatus = 'run'
    if event.key == 'a':
        app.ff.charHeadingLeft = True
        app.ff.dx = -10
        app.ff.charStatus = 'run'
    if event.key == 'w':
        if app.ff.onGround == True:
            app.ff.dy = -20
def keyReleased(app,event):
    if event.key == 'd':
        app.ff.dx = 0
        app.ff.charStatus = 'idle'
    if event.key == 'a':
        app.ff.dx = 0
        app.ff.charStatus = 'idle'
    if event.key == 'w':
        app.ff.charStatus = 'idle'
def mousePressed(app, event):#fire and change direction accordingly
    if event.x - app.ff.cx == 0:
        ang = 0.05
    else:
        ang = math.atan((event.y - app.height / 2)/(event.x - app.ff.cx))
    if abs(ang)<0.5:
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
    if abs(ang)<0.5:
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
def mouseMoved(app, event):
    if event.x - app.ff.cx == 0:
        ang = 0.5
    else:
        ang = math.atan((event.y - app.height / 2)/(event.x - app.ff.cx))
    if abs(ang)>0.5:
        app.ff.outOfFiringArc = True
    else:
        app.ff.outOfFiringArc = False
def redrawAll(app, canvas):
    drawPlatforms(app, canvas)
    drawProjectiles(app, canvas)
    drawEnemies(app, canvas)
    app.chaser.drawChaser(app, canvas)
    if app.gameOver:
        canvas.create_text(app.width / 2, app.height / 2, text = "game over",
        font = 'Arial 30 bold')
    app.ff.drawChar(app, canvas)
    app.ff.drawStats(app, canvas)
def main():
    runApp(width = 960, height = 720)

if __name__ == '__main__':
    main()
