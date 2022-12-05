import random
import pygame
import string
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (125, 125, 125)

class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def printDetail(self, my_screen, text_string, color, fontSize, xPosition, yPosition):
        """ Draw text onto the screen. """
        newFont = pygame.font.Font(None, fontSize)
        text_width, text_height = newFont.size(text_string)

        xPosition -= (text_width/2)
        yPosition -= (text_height/2)
        text_bitmap = newFont.render(text_string, True, color)
        my_screen.blit(text_bitmap, [xPosition, yPosition])

    def print(self, my_screen, text_string, color):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, color)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10
 
up = False
down = False
right = False
left = False
space = False
click = False
ctrl = False
f = False
v = False
tick = 0

##Initalizing pygame
pygame.init()

# Set the width and height of the screen [width,height]
size = [600, 750]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Invaders")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
 
# Get ready to print
textPrint = TextPrint()
 
#loading images
location = "C:/Users/dawso/OneDrive/Desktop/Program-   ming/Python Files/Fun Stuff/SpaceInvaders/Pictures/"
ship = pygame.image.load(location + "Ship.jpg")
heart = pygame.image.load(location + "Heart.jpg")
emptyHeart = pygame.image.load(location + "emptyHeart.jpg")
shot = pygame.image.load(location + "Shot.jpg")
alien1 = pygame.image.load(location + "Alien1.jpg")
alien2 = pygame.image.load(location + "Alien2.jpg")
alien3 = pygame.image.load(location + "Alien3.jpg")
alien1Shield = pygame.image.load(location + "Alien1Shield.jpg")
alien2Shield = pygame.image.load(location + "Alien2Shield.jpg")
alien3Shield = pygame.image.load(location + "Alien3Shield.jpg")
alien1Shield2 = pygame.image.load(location + "Alien1Shield2.jpg")
alien2Shield2 = pygame.image.load(location + "Alien2Shield2.jpg")
alien3Shield2 = pygame.image.load(location + "Alien3Shield2.jpg")
bossImg = pygame.image.load(location + "Boss.jpg")
barImg = pygame.image.load(location + "Barrage.jpg")
shrapnels = pygame.image.load(location + "Shrapnel.jpg")
bombs = pygame.image.load(location + "Bomb.jpg")
explosion = pygame.image.load(location + "Explosion.jpg")

# ------------ Object Methods ------------ #
class Alien(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = []
        self.y_pos = []
        self.alienShip = []
        self.bombDrop = []
        self.health = []
        self.alienKills = 0
        self.limitedAlienKills = 1
        self.gameLost = False
        self.gameStarted = False
        self.moveDirection = 1

    def clear(self):
        self.x_pos = []
        self.y_pos = []
        self.alienShip = []
        self.bombDrop = []
        self.health = []
        self.moveDirection = 1

    def newAliens(self, xAlienNum, yAlienNum, alienWidth, alienHeight, animation, startingHeight, startingX, shieldRows):
        startingX -= (xAlienNum * alienWidth)/2
        
        if animation:
            self.x_pos = []
            self.y_pos = []
            self.alienShip = []
            self.bombDrop = []
            self.health = []
        for num in range(0, xAlienNum*yAlienNum):
            self.bombDrop.append(random.randrange(0, 1000))
        count = 0
        if shieldRows > 0:
            for num in range(xAlienNum*(yAlienNum-shieldRows)):
                self.health.append(1)
            for num in range(xAlienNum*(shieldRows)):
                self.health.append(3)
        else:
            for num in range(0, xAlienNum*yAlienNum):
                self.health.append(1)
        for num in range(0, xAlienNum*yAlienNum):
            count += 1
            if self.health[num] > 1:
                self.alienShip.append(count+3)
            else:
                self.alienShip.append(count)
            if count == 3:
                count = 0
        lastRow = 0
        for num in range(0, xAlienNum*yAlienNum):
            if num%xAlienNum == 0:
                lastRow = num
            self.x_pos.append(startingX + (num-lastRow)*alienWidth)
        lastRow = 0
        for num in range(0, xAlienNum*yAlienNum):
            if num%xAlienNum == 0:
                lastRow += 1
            self.y_pos.append(startingHeight + alienHeight*lastRow)
    
    def destroy(self, index):
        self.health[index] -= 1
        if self.health[index] == 0:
            self.x_pos.pop(index)
            self.y_pos.pop(index)
            self.alienShip.pop(index)
            self.health.pop(index)
            self.alienKills += 1
            self.limitedAlienKills += 1
            return True
        return False

    def move(self, xmoveDistance, ymoveDistance):
        if len(self.x_pos) != 0:
            cond = False
            for num in range(0,len(self.x_pos)):
                if self.x_pos[num] >= size[0]-60 or self.x_pos[num] <= 30:
                    cond = True
            if cond:
                self.moveDirection *= -1
                for num in range(0,len(self.y_pos)):
                    self.y_pos[num] = self.y_pos[num] + ymoveDistance
                for num in range(0,len(self.x_pos)):
                    self.x_pos[num] = self.x_pos[num] + xmoveDistance*self.moveDirection
            else:
                for num in range(0,len(self.x_pos)):
                    self.x_pos[num] = self.x_pos[num] + xmoveDistance*self.moveDirection

            cond = False
            for num in self.y_pos:
                if num >= size[1]-150:
                    cond = True
            if cond:
                self.gameLost = True

    def newBomb(self, ticks):
        for num in range(0,len(self.x_pos)):
            if ticks == self.bombDrop[num]:
                bomb.bombsAway(self.x_pos[num]+(alien1.get_width()/2), self.y_pos[num]+alien1.get_height())

    def display(self, my_screen):
        for num in range(0,len(self.x_pos)):
            match self.alienShip[num]:
                case 1:
                    my_screen.blit(alien1, (self.x_pos[num], self.y_pos[num]))
                case 2:
                    my_screen.blit(alien2, (self.x_pos[num], self.y_pos[num]))
                case 3:
                    my_screen.blit(alien3, (self.x_pos[num], self.y_pos[num]))
                case 4:
                    if self.health[num] == 3:
                        my_screen.blit(alien1Shield, (self.x_pos[num], self.y_pos[num]))
                    elif self.health[num] == 2:
                        my_screen.blit(alien1Shield2, (self.x_pos[num], self.y_pos[num]))
                    else:
                        my_screen.blit(alien1, (self.x_pos[num], self.y_pos[num]))
                case 5:
                    if self.health[num] == 3:
                        my_screen.blit(alien2Shield, (self.x_pos[num], self.y_pos[num]))
                    elif self.health[num] == 2:
                        my_screen.blit(alien2Shield2, (self.x_pos[num], self.y_pos[num]))
                    else:
                        my_screen.blit(alien2, (self.x_pos[num], self.y_pos[num]))
                case 6:
                    if self.health[num] == 3:
                        my_screen.blit(alien3Shield, (self.x_pos[num], self.y_pos[num]))
                    elif self.health[num] == 2:
                        my_screen.blit(alien3Shield2, (self.x_pos[num], self.y_pos[num]))
                    else:
                        my_screen.blit(alien3, (self.x_pos[num], self.y_pos[num]))
alien = Alien()


class Player(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = int(size[0]/2) - ship.get_width()/2
        self.y_pos = int(size[1]-100) - ship.get_height()
        self.health = 1
        self.alive = True
        self.lastShot = 0
        self.lastTick = 0
        self.shotSide = 0

    def clear(self, restartPosition):
        if restartPosition:
            self.x_pos = int(size[0]/2)
            self.y_pos = int(size[1]-100) - ship.get_height()
        self.health = 1
        self.alive = True
        self.lastShot = 0
        self.lastTick = 0
        self.shotSide = 0

    def move(self, moveDistance, shotInterval):
        if left and not right and self.alive and self.x_pos >= 20:
            self.x_pos -= moveDistance
        if right and not left and  self.alive and self.x_pos <= size[0] - ship.get_width() - 20:
            self.x_pos += moveDistance
        if space and self.lastShot >= shotInterval and self.alive and alien.gameStarted:
            if self.shotSide != 0:
                self.shotSide += 1
                if self.shotSide > 2:
                    self.shotSide = 1
                if self.shotSide==1:
                    bullet.newShot(self.x_pos-ship.get_width()/2+shot.get_width()+2, self.y_pos+ship.get_height()-4)
                else:
                    bullet.newShot(self.x_pos+ship.get_width()/2-shot.get_width()-2, self.y_pos+ship.get_height()-4)
            else:
                 bullet.newShot(self.x_pos+ship.get_width()/2-18-shot.get_width(), self.y_pos)
            self.lastShot = 0
        if tick != self.lastTick:
            self.lastShot += 1
            self.lastTick = tick

    def die(self):
        if self.health:
            self.health -= 1
        if not self.health:
            self.alive = False
            alien.gameLost = True

    def display(self, my_screen):
        if self.alive:
            my_screen.blit(ship, (self.x_pos, self.y_pos))
        else:
            my_screen.blit(explosion, (self.x_pos, self.y_pos+ship.get_height()/4))
        for num in range(self.health):
            my_screen.blit(heart, (10 + (num* (10 + heart.get_width())), size[1]-30-heart.get_height()))
        emptyHeartWidth = heart.get_width() - int(alien.limitedAlienKills/100 * heart.get_width())
        place = (10 + (self.health*(10 + heart.get_width())), size[1]-30-heart.get_height())
        area = (0, 0, heart.get_width()-emptyHeartWidth, heart.get_height())
        my_screen.blit(emptyHeart, place)
        my_screen.blit(heart, place, area)
player = Player()


class Bullet(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = []
        self.y_pos = []

    def clear(self):
        self.x_pos = []
        self.y_pos = []

    def newShot(self, xPosition, yPosition):
        self.x_pos += [xPosition + int(ship.get_width()/2) - int(shot.get_width()/2) +1]
        self.y_pos += [yPosition - shot.get_height() +8]

    def destroy(self, index):
        self.x_pos.pop(index)
        self.y_pos.pop(index)

    def move(self, moveDistance):
        removeList = []
        for num in range(0,len(self.y_pos)):
            self.y_pos[num] = self.y_pos[num] - moveDistance
            if self.y_pos[num] < -4:
                removeList += [num]
        count = 0
        for num in removeList:
            self.destroy(num -  count)
            count += 1
        alienList = []
        removeList = []
        for num in range(0,len(self.x_pos)):
            for num2 in range(0,len(alien.y_pos)):
                cond1 = self.y_pos[num] >= alien.y_pos[num2] and self.y_pos[num] <= alien.y_pos[num2]+alien1.get_height()
                cond2 = self.x_pos[num] >= alien.x_pos[num2] and self.x_pos[num] <= alien.x_pos[num2]+alien1.get_width()
                if cond1 and cond2:
                    alienList += [num2]
                    removeList += [num]
                    continue
        #removing duplicates
        alienList = [*set(alienList)]
        removeList = [*set(removeList)]
        count = 0
        for num in range(0,len(alienList)):
            died = alien.destroy(alienList[num] - count)
            if died:
                count += 1
        if alien.limitedAlienKills >= 100:
            player.health += 1
            alien.limitedAlienKills = 1
        count = 0
        for num in range(0,len(removeList)):
            bullet.destroy(removeList[num] - count)
            count += 1
        removeList = []
        if boss.visible:
            for num in range(0,len(self.x_pos)):
                cond1 = self.y_pos[num] <= bossImg.get_height() + 60
                cond2 = self.x_pos[num] >= size[0]/2-bossImg.get_width()/2 and self.x_pos[num] <= size[0]/2+bossImg.get_width()/2
                if cond1 and cond2:
                    removeList += [num]
                    continue
            count = 0
            for num in removeList:
                bullet.destroy(num - count)
                boss.takeDamage()
                count += 1


    def display(self, my_screen):
        for num in range(0,len(self.y_pos)):
            if self.x_pos != None:
                my_screen.blit(shot, (self.x_pos[num], self.y_pos[num]))
bullet = Bullet()


class Bomb(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = []
        self.y_pos = []

    def clear(self):
        self.x_pos = []
        self.y_pos = []

    def bombsAway(self, xPosition, yPosition):
        self.x_pos += [xPosition + int(alien1.get_width()/2) - int(bombs.get_width()/2) ]
        self.y_pos += [yPosition - bombs.get_height() ]

    def destroy(self, index):
        self.x_pos.pop(index)
        self.y_pos.pop(index)

    def move(self, moveDistance):
        removeList = []
        for num in range(0,len(self.y_pos)):
            self.y_pos[num] = self.y_pos[num] + moveDistance
            if self.y_pos[num] > size[1]+10:
                removeList += [num]
        count = 0
        for num in removeList:
            self.destroy(num - count)
            count += 1
        bombList = []
        for num in range(0,len(self.x_pos)):
            cond1 = self.y_pos[num] >= size[1]-100-ship.get_height() and self.y_pos[num] <= size[1]-100
            cond2 = self.x_pos[num] >= player.x_pos-5 and self.x_pos[num] <= player.x_pos+ship.get_width()
            if cond1 and cond2:
                bombList += [num]
        count = 0
        for num in bombList:
            self.destroy(num - count)
            player.die()
            count += 1

    def display(self, my_screen):
        for num in range(0,len(self.y_pos)):
            if self.x_pos != None:
                my_screen.blit(bombs, (self.x_pos[num], self.y_pos[num]))
bomb = Bomb()


class Boss(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = (size[0]/2)-(bossImg.get_width()/2)
        self.y_pos = -10-bossImg.get_height()
        self.spawnXAmount = 0
        self.spawnYAmount = 0
        self.spawnShield = 0
        self.health = 0
        self.startingHealth = 0
        self.level = 0
        self.visible = False
        self.barrageTick = []
        self.barrageCount = 0
        self.aliensLaunched = False
        self.deathAnimation = False
        self.explX = []
        self.explY = []
        self.explCount = 0
        self.explNum = 1

    def destroy(self):
        self.x_pos = (size[0]/2)-(bossImg.get_width()/2)
        self.y_pos = -10-bossImg.get_height()
        self.numAlienLaunches = 10
        self.spawnXAmount = 0
        self.spawnYAmount = 0
        self.spawnShield = 0
        self.health = 0
        self.startingHealth = 0
        self.level = 0
        self.visible = False
        self.barrageTick = []
        self.barrageCount = 0
        self.aliensLaunched = False
        self.deathAnimation = False
        self.explX = []
        self.explY = []
        self.explCount = 0
        self.explNum = 1

    def newBoss(self, my_screen, level, tick, adone, barrageNum, xAmount, yAmount, shields, alienNum):
        self.numAlienLaunches = alienNum
        self.y_pos = -10-bossImg.get_height() + int((tick/150) * (bossImg.get_height()+60))
        self.level = level
        bullet.clear()
        bomb.clear()
        my_screen.blit(bossImg, (self.x_pos, self.y_pos))
        if self.y_pos >= (bossImg.get_height()-30):
            self.visible = True
            adone += 1
            
            self.health = 100 + ( pow(level,4) * 50)
            self.startingHealth = self.health
            self.spawnXAmount = xAmount
            self.spawnYAmount = yAmount
            self.spawnShield = shields
            self.barrageCount = 0

            self.barrageTick = []
            for num in range(0,barrageNum):
                rand = int(random.randrange(0,999))
                if len(self.barrageTick) == 0:
                    self.barrageTick += [rand]
                else:
                    cond = False
                    for ticks in range(0,len(self.barrageTick)):
                        if rand <= self.barrageTick[ticks] + 30 and rand >= self.barrageTick[ticks] - 30:
                            cond = True
                    if not cond:
                        self.barrageTick += [rand]
            alien.gameStarted = True

        return adone

    def takeDamage(self):
        self.health -= 1

    def newAlienSpawns(self, alienWidth, alienHeight):
        startingX = (size[0]/2) - (self.spawnXAmount * alienWidth/4)
        startingY = bossImg.get_height()+alien1.get_height()
        
        alien.newAliens(self.spawnXAmount, self.spawnYAmount, alienWidth, alienHeight, False, startingY, startingX, self.spawnShield)

    def newBarrage(self):
        rand = int(random.randrange(int(size[0]/2-bossImg.get_width()/2), int(size[0]/2+bossImg.get_width()/2)))
        barrage.bombsAway(rand)

    def runBoss(self, ticks, my_screen):
        if self.health == 0 and not self.deathAnimation:
            barrage.clear()
            alien.clear()
            bomb.clear()
            shrapnel.clear()
            self.deathAnimation = True
            self.explX = [None] * 4
            self.explY = [None] * 4
            self.explX[0] = random.randrange(int(size[0]/2 - bossImg.get_width()/2-explosion.get_width()), int(size[0]/2))
            self.explY[0] = random.randrange(60, 30+int(bossImg.get_height()/2))
            self.explX[1] = random.randrange(int(size[0]/2), int(size[0]/2 + bossImg.get_width()/2))
            self.explY[1] = random.randrange(60+int(bossImg.get_height()/2), 30+bossImg.get_height())
            self.explX[2] = random.randrange(int(size[0]/2 - bossImg.get_width()/2-explosion.get_width()), int(size[0]/2))
            self.explY[2] = random.randrange(60, 30+int(bossImg.get_height()/2))
            self.explX[3] = random.randrange(int(size[0]/2), int(size[0]/2 + bossImg.get_width()/2))
            self.explY[3] = random.randrange(60+int(bossImg.get_height()/2), 30+bossImg.get_height())
        
        if self.deathAnimation:
            my_screen.blit(bossImg, (self.x_pos, self.y_pos))
            if self.explCount%40 == 0:
                self.explNum += 1
            if self.explNum < 5:
                for num in range(0, len(self.explX)-int(4-self.explNum)):
                    my_screen.blit(explosion, (self.explX[num], self.explY[num]))
            else:
                for num in range(0, 4):
                    my_screen.blit(explosion, (self.explX[num], self.explY[num]))
            if self.explNum == 6:
                self.destroy()
            self.explCount += 1

        else:
            barrage.move(2, my_screen)
            for num in self.barrageTick:
                if num == ticks:
                    self.newBarrage()
                    self.barrageCount += 1
                    self.aliensLaunched = False
                    break
            if self.barrageCount%self.numAlienLaunches == 0 and not self.aliensLaunched and self.barrageCount != 0:
                self.newAlienSpawns(30, 30)
                self.aliensLaunched = True

    def display(self, my_screen):
        if self.visible:
            barrage.display(my_screen)
            my_screen.blit(bossImg, (self.x_pos, self.y_pos))
            pygame.draw.rect(screen, GRAY, [20, 10, size[0]-40, 25])
            pygame.draw.rect(screen, RED, [24, 14, int( ( self.health/self.startingHealth ) * (size[0]-48) ), 17])
boss = Boss()
class Barrage(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = []
        self.y_pos = []

    def clear(self):
        self.x_pos = []
        self.y_pos = []

    def bombsAway(self, xPosition):
        yPosition = bossImg.get_height()
        self.x_pos += [xPosition - int(barImg.get_width()/2) ]
        self.y_pos += [yPosition - bombs.get_height() ]

    def destroy(self, index):
        self.x_pos.pop(index)
        self.y_pos.pop(index)

    def move(self, moveDistance, my_screen):
        removeList = []
        for num in range(0,len(self.y_pos)):
            self.y_pos[num] = self.y_pos[num] + moveDistance
            if self.y_pos[num] > size[1]/2 and random.randrange(0, 30) == 5:
                removeList += [num]
                shrapnel.shrapnelSpawn(self.x_pos[num] + barImg.get_width()/2, self.y_pos[num] + barImg.get_height()/2)
                my_screen.blit(explosion, (self.x_pos[num] + barImg.get_width()/2, self.y_pos[num] + barImg.get_height()/2))
        count = 0
        for num in removeList:
            self.destroy(num - count)
            count += 1
        shrapnel.move(7)

    def display(self, my_screen):
        for num in range(0,len(self.y_pos)):
            if self.x_pos != None:
                my_screen.blit(barImg, (self.x_pos[num], self.y_pos[num]))
        shrapnel.display(my_screen)
barrage = Barrage()
class Shrapnel(object):
    def __init__(self):
        """ Constructor """
        self.x_pos = []
        self.y_pos = []
        self.direction = []

    def clear(self):
        self.x_pos = []
        self.y_pos = []
        self.direction = []

    def shrapnelSpawn(self, xPosition, yPosition):
        self.x_pos += [xPosition - int(shrapnels.get_width()/2) ] * 3
        self.y_pos += [yPosition - bombs.get_height() ] * 3
        for num in range(-1,2):
            self.direction += [num]

    def destroy(self, index):
        self.x_pos.pop(index)
        self.y_pos.pop(index)
        self.direction.pop(index)

    def move(self, moveDistance):
        removeList = []
        for num in range(0,len(self.y_pos)):
            self.y_pos[num] += moveDistance
            self.x_pos[num] += self.direction[num]*(moveDistance/2)
            if self.y_pos[num] > size[1]+10:
                removeList += [num]
        count = 0
        for num in removeList:
            self.destroy(num-count)
            count+=1

        bombList = []
        for num in range(0,len(self.x_pos)):
            cond1 = self.y_pos[num] >= size[1]-100-ship.get_height() and self.y_pos[num] <= size[1]-100
            cond2 = self.x_pos[num] >= player.x_pos-5 and self.x_pos[num] <= player.x_pos+ship.get_width()
            if cond1 and cond2:
                bombList += [num]
        count = 0
        for num in bombList:
            self.destroy(num-count)
            player.die()
            count+=1

    def display(self, my_screen):
        for num in range(0,len(self.y_pos)):
            if self.x_pos != None:
                my_screen.blit(shrapnels, (self.x_pos[num], self.y_pos[num]))
shrapnel = Shrapnel()

class leaderboard(object):
    def __init__(self):
        self.leaderList = []
        self.grabLeaders()
        self.leaderList.sort()
        self.leaderList.reverse()

    def grabLeaders(self):
        with open("leaderboard.txt") as self.leaderFile:
            self.leaderList = []
            for player in self.leaderFile.readlines():
                for index in range(0,len(player)):
                    if player[index] == "-":
                        strings = player[int(0):int(index-1)]
                        score = int(player[int(index+2):len(player)-1])
                        self.leaderList.append( (score, strings) )

    def add(self, name, score):
        newPlayer = True
        index = 0
        for player in self.leaderList:
            if name == player[1]:
                if player[0] < score:
                    self.leaderList[index] = (score, name)
                newPlayer = False
            index += 1
        if newPlayer:
            self.leaderList.append( (score, name) )
        self.leaderList.sort()
        self.leaderList.reverse()
        if len(self.leaderList) > 15:
            self.leaderList.pop(15)
        with open("leaderboard.txt", "w") as self.leaderFile:
            strings = ""
            for player in self.leaderList:
                strings += player[1] + " - " + str(player[0]) + "\n"
            self.leaderFile.write(strings)

    def display(self, my_screen):
        textPrint.printDetail(my_screen, "Leaderboard", WHITE, 28, size[0]/2, 153)
        pygame.draw.line(my_screen, WHITE, (size[0]/2-65, 166), (size[0]/2+65, 166))
        textPrint.printDetail(my_screen, "Player Name", WHITE, 24, size[0]/2-70, 190)
        textPrint.printDetail(my_screen, "Score", WHITE, 24, size[0]/2+70, 190)
        if not len(self.leaderList):
            textPrint.printDetail(my_screen, "No leaderboard players yet", WHITE, 20, size[0]/2, 205)
        num = 0
        for player in self.leaderList:
            textPrint.printDetail(my_screen, player[1], WHITE, 20, size[0]/2-70, 215 + 15*num)
            textPrint.printDetail(my_screen, str(player[0]), WHITE, 20, size[0]/2+70, 215 + 15*num)
            num += 1
leaderBoard = leaderboard()

def newWave(alienX, alienY, alienWidth, alienHeight, startingX, aDone, shieldRows):
    bullet.clear()
    bomb.clear()
    yValue = -(2 * alienX * alienY) + int((tick/60) * (alienX * alienY))
    alien.newAliens(alienX, alienY, alienWidth, alienHeight, True, yValue, startingX, shieldRows)
    if (yValue >= -10):
        alien.gameStarted = True
        aDone += 1
    return aDone


# -------- Main Program Loop ----------
#loop variables
movingDistance = 5
pressed = False
joystickDisconnected = True
healthAdded = False
justWon = False
animationDone = 0
wave = 1
lastKill = 0
waveScore = 0
totalScore = 0
typing = True
letter = 1
newName = [0, 0, 0]
shootSpeed = 5
bef = -50
aft = 0
while not done:
    #getting joystick count
    joystick_count = pygame.joystick.get_count()

    # DRAWING STEP
    # First, clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    textPrint.reset()
    
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

        if joystick_count == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = True
                if event.key == pygame.K_SPACE:
                    space = True
                if event.key == pygame.K_LCTRL:
                    ctrl = not ctrl
                if event.key == pygame.K_f:
                    f = not f
                if event.key == pygame.K_v:
                    v = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_SPACE:
                    space = False
                if event.key == pygame.K_v:
                    v = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False

    #getting joystick input
    try:
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            joystickDisconnected = True

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            joystickDistance = int( joystick.get_axis(0)*10 ) / 10
            movingDistance = math.sqrt( pow(5*joystickDistance,2) )
            if joystick.get_axis(0) > 0:
                right = True
                left = False
            if joystick.get_axis(0) < 0:
                right = False
                left = True

            if joystick.get_button(0) == 1 and not pressed:
                space = True
                pressed = True
            elif joystick.get_button(0) == 0:
                space = False
                pressed = False
        elif joystickDisconnected:
            movingDistance = 5
            right = False
            left = False
            joystickDisconnected = False
    except:
        1
 
    #Drawing objects
    player.display(screen)
    pygame.draw.line(screen, GREEN, (0, size[1]-100), (size[0], size[1]-100))
    alien.display(screen)
    bullet.display(screen)
    bomb.display(screen)
    if boss.visible:
        boss.display(screen)
        boss.runBoss(tick, screen)

    ##Printing/acting steps
    if (ctrl and f):
        if (up):
            textPrint.print(screen, "Up is pressed", WHITE)
        else:
            textPrint.print(screen, "No up", WHITE)
        if (down):
            textPrint.print(screen, "Down is pressed", WHITE)
        else:
            textPrint.print(screen, "No down", WHITE)
        if (left):
            textPrint.print(screen, "Left is pressed", WHITE)
        else:
            textPrint.print(screen, "No left", WHITE)
        if (right):
            textPrint.print(screen, "Right is pressed", WHITE)
        else:
            textPrint.print(screen, "No right", WHITE)
        if (space):
            textPrint.print(screen, "Space is pressed", WHITE)
        else:
            textPrint.print(screen, "No space", WHITE)
        if (click):
            textPrint.print(screen, "Click is pressed", WHITE)
        else:
            textPrint.print(screen, "No click", WHITE)
        textPrint.print(screen, "", WHITE)
        textPrint.print(screen, "{} Ticks".format(tick), WHITE)
        textPrint.print(screen, "{} Aliens".format(len(alien.x_pos)), WHITE)
        textPrint.print(screen, "{} Shots".format(len(bullet.x_pos)), WHITE)
        textPrint.print(screen, "{} Bombs".format(len(bomb.x_pos)), WHITE)
        textPrint.print(screen, "{} Barrages".format(len(barrage.x_pos)), WHITE)
        textPrint.print(screen, "{} Shrapnel".format(len(shrapnel.x_pos)), WHITE)
        textPrint.print(screen, "{} AnimationDone".format(animationDone), WHITE)
        textPrint.print(screen, "{} Wave".format(wave), WHITE)
        textPrint.print(screen, "{} Score".format(totalScore + waveScore), WHITE)
    #if (ctrl and space and up):
    #    alien.clear()
    #    up = False
    
    #Menu Decisions/Prints
    sep = 40
    change = 150
    if tick%sep == 0:
        aft = tick
        if bef == 0:
            bef = sep
        else:
            bef = 0
    if bef == 0:
        color = (255-int((tick-aft)/sep*change), 255-int((tick-aft)/sep*change), 255-int((tick-aft)/sep*change))
    else:
        color = (255-int((bef-(tick-aft))/sep*change), 255-int((bef-(tick-aft))/sep*change), 255-int((bef-(tick-aft))/sep*change))
    r,g,b = color
    if r > 255:
        r = 255
    elif r < 0:
        r = 0
    if g > 255:
        g = 255
    elif g < 0:
        g = 0
    if b > 255:
        b = 255
    elif b < 0:
        b = 0
    color = (r, g, b)
        
    if not alien.gameStarted:
        if animationDone == 0:
            textPrint.printDetail(screen, "Space Invaders", WHITE, 50, size[0]/2, 100)
            leaderBoard.display(screen)
            if joystick_count == 0:
                textPrint.printDetail(screen, "Hit space to begin", color, 22, size[0]/2, (size[1]-100)/2+180)
            if joystick_count > 0:
                textPrint.printDetail(screen, "Hit A to begin", color, 22, size[0]/2, (size[1]-100)/2-180)
        elif animationDone == -2:
            tick = 0
            animationDone = -1
            space = False
            typing = True
        elif animationDone == -1 and not typing:
            if justWon:
                textPrint.printDetail(screen, "Game Won", WHITE, 50, size[0]/2, (size[1]-100)/2-120)
            else:
                textPrint.printDetail(screen, "Game Lost", WHITE, 50, size[0]/2, (size[1]-100)/2-120)
            textPrint.printDetail(screen, "You killed {} aliens".format(alien.alienKills), WHITE, 50, size[0]/2, (size[1]-100)/2-60)
            textPrint.printDetail(screen, "with a score of {}".format(totalScore), WHITE, 50, size[0]/2, (size[1]-100)/2)
            if joystick_count == 0:
                textPrint.printDetail(screen, "Hit space to go back to title screen", WHITE, 20, size[0]/2, (size[1]-100)/2+150)
            if joystick_count > 0:
                textPrint.printDetail(screen, "Hit A to go back to title screen", WHITE, 20, size[0]/2, (size[1]-100)/2+150)
            savable = False
            if len(leaderBoard.leaderList) < 15:
                savable = True
            for leader in leaderBoard.leaderList:
                if leader[0] < totalScore:
                    savable = True
            if savable:
                textPrint.printDetail(screen, "Hit V to save on leaderboard", WHITE, 20, size[0]/2, (size[1]-100)/2+165)
            if space:
                space = False
                animationDone = 0
                alien.alienKills = 0
                alien.limitedAlienKills = 1
                alien.gameLost = False
                alien.gameStarted = False
                wave = 0
                player.clear(True)
                bullet.clear()
                bomb.clear()
                alien.clear()
                barrage.clear()
                shrapnel.clear()
                boss.visible = False
            if v and savable:
                v = False
                typing = True
        elif animationDone == -1 and typing:
            if justWon:
                textPrint.printDetail(screen, "Game Won", WHITE, 50, size[0]/2, (size[1]-100)/2-120)
            else:
                textPrint.printDetail(screen, "Game Lost", WHITE, 50, size[0]/2, (size[1]-100)/2-120)
            textPrint.printDetail(screen, "You killed {} aliens".format(alien.alienKills), WHITE, 50, size[0]/2, (size[1]-100)/2-60)
            textPrint.printDetail(screen, "with a score of {}".format(totalScore), WHITE, 50, size[0]/2, (size[1]-100)/2)
            if joystick_count == 0:
                textPrint.printDetail(screen, "Hit space to go back to title screen", WHITE, 20, size[0]/2, (size[1]-100)/2+180)
            if joystick_count > 0:
                textPrint.printDetail(screen, "Hit A to go back to title screen", WHITE, 20, size[0]/2, (size[1]-100)/2+180)
            textPrint.printDetail(screen, "Hit V to not save on leaderboard", WHITE, 20, size[0]/2, (size[1]-100)/2+165)
            if v:
                v = False
                typing = False
            if left:
                left = False 
                letter -= 1
                if letter <= 0:
                    letter = 3
            if right:
                right = False
                letter += 1
                if letter > 3:
                    letter = 1
            if up:
                up = False
                newName[letter-1] += 1
                if newName[letter-1] > 25:
                    newName[letter-1] = 0
            if down:
                down = False
                newName[letter-1] -= 1
                if newName[letter-1] < 0:
                    newName[letter-1] = 25
            if space:
                strings = string.ascii_uppercase[newName[0]] + string.ascii_uppercase[newName[1]] + string.ascii_uppercase[newName[2]]
                leaderBoard.add(strings, totalScore)
                space = False
                animationDone = 0
                alien.alienKills = 0
                alien.limitedAlienKills = 1
                alien.gameLost = False
                alien.gameStarted = False
                wave = 0
                player.clear(True)
                bullet.clear()
                bomb.clear()
                alien.clear()
                barrage.clear()
                shrapnel.clear()
                boss.visible = False
            match (letter):
                case 1:
                    move = -77
                case 2:
                    move = 0
                case 3:
                    move = 77
            nameString = string.ascii_uppercase[newName[0]] + "   " + string.ascii_uppercase[newName[1]] + "   " + string.ascii_uppercase[newName[2]]
            textPrint.printDetail(screen, nameString, WHITE, 70, size[0]/2, (size[1]-100)/2+85)
            pygame.draw.line(screen, color, (size[0]/2-20+move,(size[1]-100)/2+120), (size[0]/2+20+move,(size[1]-100)/2+120), 3)

        if space and animationDone == 0:
            animationDone = 1
            wave = 1
            tick = 0
            totalScore = 0
            waveScore = 0
            lastKill = 0

    #Wave Detection
    if ( (animationDone%2 != 0 and animationDone > 0) or animationDone == 12) and animationDone != 23:
        if wave%5 != 0 and animationDone%11 != 0:
            textPrint.printDetail(screen, "Wave {}".format(wave), WHITE, 50, size[0]/2, (size[1]-100)/2-60)
        elif animationDone%11 != 0:
            textPrint.printDetail(screen, "Boss {}".format(int(wave/5)), RED, 50, size[0]/2, (size[1]-100)/2-60)

        if animationDone%11 != 0:
            match wave:
                case 1:
                    animationDone = newWave(10, 5, 30, 30, size[0]/2, animationDone, 0)
                    shootSpeed = 20
                case 2:
                    animationDone = newWave(7, 10, 30, 30, size[0]/2, animationDone, 0)
                    shootSpeed = 15
                case 3:
                    animationDone = newWave(12, 8, 30, 30, size[0]/2, animationDone, 0)
                    shootSpeed = 10
                case 4:
                    animationDone = newWave(25, 3, 20, 30, size[0]/2, animationDone, 0)
                    shootSpeed = 5
                case 5:
                    animationDone = boss.newBoss(screen, 1, tick, animationDone, 17, 7, 2, 0, 8)
                    player.shotSide = 1
                    shootSpeed = 8
                case 6:
                    animationDone = newWave(10, 5, 30, 30, size[0]/2, animationDone, 2)
                    shootSpeed = 6
                case 7:
                    animationDone = newWave(8, 12, 30, 30, size[0]/2, animationDone, 8)
                    shootSpeed = 5
                case 8:
                    animationDone = newWave(12, 8, 30, 30, size[0]/2, animationDone, 8)
                    shootSpeed = 3
                case 9:
                    animationDone = newWave(23, 5, 20, 26, size[0]/2, animationDone, 3)
                    shootSpeed = 2
                case 10:
                    animationDone = boss.newBoss(screen, 2, tick, animationDone, 40, 10, 2, 2, 5)
                    shootSpeed = 2
    if (animationDone == 11 or animationDone == 23) and animationDone:
        bullet.clear()
        bomb.clear()
        alien.clear()
        barrage.clear()
        shrapnel.clear()
        textPrint.printDetail(screen, "Part {} Won!".format(int(wave/5)), WHITE, 50, size[0]/2, (size[1]-100)/2-120)
        textPrint.printDetail(screen, "You killed {} Aliens".format(alien.alienKills), WHITE, 50, size[0]/2, (size[1]-100)/2-60)
        textPrint.printDetail(screen, "and", WHITE, 50, size[0]/2, (size[1]-100)/2-23)
        textPrint.printDetail(screen, "Successfully Beat {} Boss!".format(int(wave/5)), WHITE, 50, size[0]/2, (size[1]-100)/2+26)
        if animationDone == 11:
            if joystick_count == 0:
                textPrint.printDetail(screen, "Hit space to continue", WHITE, 20, size[0]/2, (size[1]-100)/2+80)
            if joystick_count > 0:
                textPrint.printDetail(screen, "Hit A to continue", WHITE, 20, size[0]/2, (size[1]-100)/2+80)
            if space and not justWon:
                tick = 0
                animationDone += 1
                boss.visible = False
                justWon = True
            elif not space:
                justWon = False
        else:
            if joystick_count == 0:
                textPrint.printDetail(screen, "Hit space to Save Score", WHITE, 20, size[0]/2, (size[1]-100)/2+80)
            if joystick_count > 0:
                textPrint.printDetail(screen, "Hit A to Save Score", WHITE, 20, size[0]/2, (size[1]-100)/2+80)
            if space and not justWon:
                tick = 0
                totalScore += 5000
                boss.visible = False
                justWon = True
                alien.gameLost = True
                typing = True
            elif not space:
                justWon = False
                
    if alien.alienKills != lastKill:
        lastKill = alien.alienKills
        waveScore = lastKill*wave
    if len(alien.x_pos) == 0 and alien.gameStarted and player.alive and animationDone not in [9, 11, 12, 19, 21, 23] and not boss.visible:
        tick = 0
        animationDone += 1
        wave += 1
        totalScore += waveScore
        waveScore = 0
        justWon = True

    #Object Decisions
    if (animationDone%2==0 and animationDone > 1) or animationDone == -1:
        alien.move(3, 24)
        alien.newBomb(tick)
        player.move(movingDistance, shootSpeed)
        bullet.move(8)
        bomb.move(4)
    else:
        player.move(movingDistance, 10001)

    if alien.gameLost and animationDone > 1:
        animationDone = -2
        totalScore += waveScore
        alien.gameStarted = False

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)
    tick += 1
    if (tick == 1000):
        tick = 0
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
