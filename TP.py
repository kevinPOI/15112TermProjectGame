#name: Kevin Tang
#andrewID: zhenrant
#images of chibi characters from game http://gf.sunborngame.com/
#gifs extracted by: https://gfl.zzzzz.kr/doll.php?id=103&lang=en
#I screen captured them, converted them to frames, and have backgrounds removed
#the character cg from https://www.pixiv.net/en/artworks/70992896\
#cmu_112_graphics modified from http://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
#explosion.png: https://www.pngitem.com/middle/hRbobiw_explosion-sprite-sheet-png-transparent-png/
#

from PIL import Image
from PIL import ImageTk
from cmu_112_graphics_mod import *

from Character import *
from PhysicalObjects import *
import math
from Miscellaneous import *

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
def generateMap(app, x, y):#procedure generation of map
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
def splashScreen(app):
    leftA = app.width / 2 - 80
    rightA = app.width / 2 + 80
    app.startB = Button(leftA, 360, rightA, 400, "Start")
    app.charB = Button(leftA, 440, rightA, 480, "Character")
def characterPage(app):
    app.returnB2 = Button(app.width - 240, 40, app.width - 40, 80, "Return to Main")
    app.hpE = Enhancement(50, app.height - 80, "HP")
    app.regenE = Enhancement(200, app.height - 80, "HP Regen")
    app.dmgE = Enhancement(350, app.height - 80, "DMG")
    app.ammoE = Enhancement(500, app.height - 80, "Ammo Ct")
    app.grenadeE = Enhancement(650, app.height - 80, "Grenade Ct")
    app.cg = Image.open("cg.png")
    app.cg = app.cg.resize((400,560))
    with open('save.txt', 'r') as reader:
        data = [line.rstrip('\n') for line in reader]
    for i in range (len(data)):
        data[i] = int(data[i])
    (app.hpE.lv, app.regenE.lv, app.dmgE.lv, app.ammoE.lv, app.grenadeE.lv,app.bestScore) = tuple(data)
def gameOverPage(app):
    leftA = app.width / 2 - 120
    rightA = app.width / 2 + 120
    app.returnB1 = Button(leftA, 620, rightA, 680, "Return to Main")
##################################################
def appStarted(app):
    app.gameStatus = 'start'
    app.ff = Character()
    (app.width, app.height) = (960, 720)
    app.platforms = []
    app.enemies = []
    app.bots = []
    splashScreen(app)
    generateMap(app, app.width / 2, 300)
    app.projectiles = []
    app.mouseAng = 0
    app.charData = []
    app.chaserData = [] 
    splashScreen(app)
    app.bestScore = 0
    characterPage(app)
    app.gameCounter = 0
    app.rp = app.hpE.lv +app.regenE.lv + app.dmgE.lv + app.ammoE.lv+app.grenadeE.lv
    gameOverPage(app)
    createChaser(app)

    for i in range (0, 10):
        app.bots.append(Bot(500, 800 + i * 600))
    app.ff.hp = 100 + 30 * app.hpE.lv
    app.ff.regen = 0 + 3 * app.regenE.lv
    app.ff.dmg = 10 + 3 * app.dmgE.lv
    app.ff.ammoCount = 30 + 12 * app.ammoE.lv
    app.ff.grenadeCount = 5 + 2 * app.grenadeE.lv
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

    
def moveProjectiles(app):#update velocity and position of projectiles
    i = 0
    while i < len(app.projectiles): 
        if type(app.projectiles[i]) == Grenade:
            grenade = app.projectiles[i]
            if grenade.explode:
                grenade.explodeCounter += 1
                if grenade.explodeCounter > 2:
                    grenade.detonate(app)
                    app.projectiles.pop(i)
                    i -= 1
            else:
                app.projectiles[i].move(app)
                
        else:
            app.projectiles[i].move(app)
        if app.projectiles[i].remove == True:
            app.projectiles.pop(i)
            i -= 1
        i += 1
def relativeY(app, y):#convert y for drawing
    diff = y - app.ff.cy  
    return app.height / 2 + diff
def timerFired(app):
    if app.gameStatus == 'run':
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
        if app.gameCounter > 10:
            app.charData.append(app.ff.cy)
            app.chaserData.append(app.chaser.y)
            app.gameCounter = 0
        app.gameCounter += 1
def keyPressed(app, event):
    if app.gameStatus == 'run':
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
    if app.gameStatus == 'run':
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
    if app.gameStatus == 'start':
        if app.startB.clicked(event.x, event.y):
            app.gameStatus = 'run'
            print (app.ff.hp, app.hpE.lv)
        if app.charB.clicked(event.x, event.y):
            app.gameStatus = 'char'
    if app.gameStatus == 'over':
        if app.returnB1.clicked(event.x, event.y):
            data = (app.hpE.lv, app.regenE.lv, app.dmgE.lv, app.ammoE.lv, app.grenadeE.lv, app.bestScore)
            data = list(data)
            for i in range (len(data)):
                data[i] = str(data[i])
            with open('save.txt', 'w') as writer:
                for e in data:
                    writer.write(e + "\n")
            appStarted(app)
            print(app.charData)
        print(app.chaserData)
            
    if app.gameStatus == 'char':
        if app.returnB2.clicked(event.x, event.y):
            app.gameStatus = 'start'

    if (app.hpE.minusClicked(event.x, event.y, app) or 
        app.regenE.minusClicked(event.x, event.y, app) or
        app.dmgE.minusClicked(event.x, event.y, app) or
        app.ammoE.minusClicked(event.x, event.y, app) or
        app.grenadeE.minusClicked(event.x, event.y, app)):
        app.ff.hp = 100 + 30 * app.hpE.lv
        app.ff.regen = 0 + 3 * app.regenE.lv
        app.ff.dmg = 10 + 3 * app.dmgE.lv
        app.ff.ammoCount = 30 + 12 * app.ammoE.lv
        app.ff.grenadeCount = 5 + 2 * app.grenadeE.lv
        data = (app.hpE.lv, app.regenE.lv, app.dmgE.lv, app.ammoE.lv, app.grenadeE.lv, app. bestScore)
        data = list(data)
        for i in range (len(data)):
            data[i] = str(data[i])
        with open('save.txt', 'w') as writer:
            for e in data:
                writer.write(e + "\n")
    if (app.hpE.plusClicked(event.x, event.y, app) or 
        app.regenE.plusClicked(event.x, event.y, app) or
        app.dmgE.plusClicked(event.x, event.y, app) or
        app.ammoE.plusClicked(event.x, event.y, app) or
        app.grenadeE.plusClicked(event.x, event.y, app)):
        app.ff.hp = 100 + 30 * app.hpE.lv
        app.ff.regen = 0 + 3 * app.regenE.lv
        app.ff.dmg = 10 + 3 * app.dmgE.lv
        app.ff.ammoCount = 30 + 12 * app.ammoE.lv
        app.ff.grenadeCount = 5 + 2 * app.grenadeE.lv
        data = (app.hpE.lv, app.regenE.lv, app.dmgE.lv, app.ammoE.lv, app.grenadeE.lv, app.bestScore)
        data = list(data)
        for i in range (len(data)):
            data[i] = str(data[i])
        with open('save.txt', 'w') as writer:
            for e in data:
                writer.write(e + "\n")
        


def rightMousePressed(app, event):
    if app.gameStatus == 'run':
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
                app.ff.launch(app, ang)
                app.mouseAng = ang
def rightMouseReleased(app, event):
    for projectile in app.projectiles:
        if type(projectile) == Grenade:
            projectile.explode = True
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
    if abs(ang)>1:
        app.ff.launcherOutOfFiringArc = True
    else:
        app.ff.launcherOutOfFiringArc = False
def redrawAll(app, canvas):
    gameStatus = app.gameStatus
    if gameStatus == 'run':
        drawPlatforms(app, canvas)
        drawProjectiles(app, canvas)
        drawEnemies(app, canvas)
        app.chaser.drawChaser(app, canvas)
        
        app.ff.drawChar(app, canvas)
        app.ff.drawStats(app, canvas)
    if gameStatus == 'over':
        canvas.create_text(app.width / 4, app.height / 4, text = "game over",
        font = 'Arial 30 bold')
        canvas.create_text(app.width / 4, app.height / 4 + 60, text = f"score: {int(app.ff.cy)}",
        font = 'Arial 16 bold', fill = 'orange')
        canvas.create_text(app.width / 4, app.height / 4 + 120, text = f"best score: {int(app.bestScore)}",
        font = 'Arial 16 bold', fill = 'black')
        app.returnB1.drawButton(canvas)
        drawChart(400,150,app,canvas)
        
    if gameStatus == 'start':
        app.startB.drawButton(canvas)
        app.charB.drawButton(canvas)
        canvas.create_text(app.width / 2 + 50, app.height / 5, text = "Down with Physics v1.0",
        font = 'Arial 40 bold')
    if gameStatus == 'char':
        app.returnB2.drawButton(canvas)
        app.hpE.drawEnhancement(canvas)
        app.regenE.drawEnhancement(canvas)
        app.dmgE.drawEnhancement(canvas)
        app.ammoE.drawEnhancement(canvas)
        app.grenadeE.drawEnhancement(canvas)
        im_tk = ImageTk.PhotoImage(app.cg)
        canvas.create_image(200, 280, image = im_tk)
        rpMax = min(12, int(app.bestScore / 600))
        canvas.create_text(app.width - 150, 600, text = f"Research Points: {app.rp} / {rpMax}",font = 'Calibri 20')
        canvas.create_text(550, 100, text = f"Hit Points: {app.ff.hp}",font = 'Calibri 20',fill = "orange")
        canvas.create_text(550, 170, text = f"HP Regen / kill: {app.ff.regen}",font = 'Calibri 20',fill = "orange")
        canvas.create_text(550, 240, text = f"Base Damage: {app.ff.dmg}",font = 'Calibri 20',fill = "orange")
        canvas.create_text(550, 310, text = f"Ammo Count: {app.ff.ammoCount}",font = 'Calibri 20',fill = "orange")
        canvas.create_text(550, 380, text = f"Grenade Count: {app.ff.grenadeCount}",font = 'Calibri 20',fill = "orange")
def main():
    runApp(width = 960, height = 720)

if __name__ == '__main__':
    main()
