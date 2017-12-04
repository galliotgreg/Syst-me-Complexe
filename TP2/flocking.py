#!/usr/bin/env python
# Boid implementation in Python using PyGame
# Ben Dowling - www.coderholic.com

import sys, pygame, random, math
from pygame import *
from math import sqrt

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

maxVelocity = 10
numBoids = 50
numMurs = 10
boids = []
murs=[]

followPlayer = False

class Pig(pygame.sprite.Sprite):
    def __init__(self, x,y,z):
        super().__init__()
        self.x = x
        self.y = y

        self.image = pygame.image.load("pig.png").convert_alpha()
        self.rect = self.image.get_rect()


class Mur(pygame.sprite.Sprite):
    def __init__(self, x,y,z):
        super().__init__()
        self.x = x
        self.y = y

        self.image = pygame.image.load("mur.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        murs.append(self)


class Boid(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.velocityX = random.randint(1, 10) / 100.0
        self.velocityY = random.randint(1, 10) / 100.0

        self.image = pygame.image.load("chuck(1).png").convert_alpha()
        self.rect = self.image.get_rect()
        self.isColliding = False

    "Return the distance from another boid"
    def distance(self, boid):
        distX = self.x - boid.x
        distY = self.y - boid.y        
        return sqrt(distX * distX + distY * distY)

    "Move closer to a set of boids"
    def moveCloser(self, boids):
        if len(boids) < 1: return
            
        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.x == self.x and boid.y == self.y:
                continue
                
            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
       
        self.velocityX -= (avgX / 100) 
        self.velocityY -= (avgY / 100)


    def moveCloserPlayer(self, pig):
        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0

        avgX += (self.x - pig.x)
        avgY += (self.y - pig.y)

        # set our velocity towards the others

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)


    "Move with a set of boids"
    def moveWith(self, boids):
        if len(boids) < 1: return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0
                
        for boid in boids:
            avgX += boid.velocityX
            avgY += boid.velocityY

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)
    
    "Move away from a set of boids. This avoids crowding"
    def moveAway(self, boids, minDistance):
        if len(boids) < 1: return
        
        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:
            distance = self.distance(boid)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.x - boid.x) 
                ydiff = (self.y - boid.y) 
                
                if xdiff >= 0: xdiff = sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -sqrt(minDistance) - xdiff
                
                if ydiff >= 0: ydiff = sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -sqrt(minDistance) - ydiff

                distanceX += xdiff 
                distanceY += ydiff 
        
        if numClose == 0:
            return
            
        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    def compute_penetration(self, mur, old_rect, new_rect):

        dx_correction = dy_correction = 0.0
        if old_rect.bottom <= mur.top < new_rect.bottom:
            dy_correction = mur.top - new_rect.bottom
        elif old_rect.top >= mur.bottom > new_rect.top:
            dy_correction = mur.bottom - new_rect.top
        if old_rect.right <= mur.left < new_rect.right:
            dx_correction = mur.left - new_rect.right
        elif old_rect.left >= mur.right > new_rect.left:
            dx_correction = mur.right - new_rect.left
        return dx_correction, dy_correction



    "Perform actual movement based on our velocity"
    def move(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        old_rect = Rect(self.rect)
        self.x += self.velocityX
        self.y += self.velocityY
        self.rect.x = self.x
        self.rect.y = self.y
        new_rect = Rect(self.rect)

#==============================================================================================================

        # Début rebond contre les murs/obstacles
        for mur in murs:
            murRect = pygame.Rect(mur.rect)
            if new_rect.colliderect(murRect):
                dx_correction, dy_correction = boid.compute_penetration(murRect, old_rect, new_rect)

                if dx_correction == 0.0:
                    new_rect.top += dy_correction
                elif dy_correction == 0.0:
                    new_rect.left += dx_correction

                if dx_correction == dy_correction == 0.0:
                    # Finalement plus de pénétration. Le new_rect a bougé précédemment
                    # lors d'une résolution de collision
                    continue
                if abs(dx_correction) < abs(dy_correction):
                    # Faire la correction que sur l'axe X (plus bas)
                    dy_correction = 0.0
                elif abs(dy_correction) < abs(dx_correction):
                    # Faire la correction que sur l'axe Y (plus bas)
                    dx_correction = 0.0
                if dy_correction != 0.0:
                    new_rect.top += dy_correction
                    vy = 0.0
                elif dx_correction != 0.0:
                    new_rect.left += dx_correction
                    vx = 0.0


        # Fin rebond mur
                boid.velocityX = -boid.velocityX * random.random() * 1000
                boid.velocityY = -boid.velocityY * random.random() * 1000

#==============================================================================================================


def creation_murs(nb_murs):
    for i in range(0,nb_murs):
        x_rand = random.randint(0,width)
        y_rand = random.randint(0,height)
        Mur(x_rand, y_rand, 0)

def afficher_murs():
    for mur in murs :
        screen.blit(mur.image, mur.rect)



screen = pygame.display.set_mode(size)

fond = pygame.image.load("background.png").convert()


creation_murs(numMurs)
#mur = Mur(100,100,0)
#mur2 = Mur(120,100,0)



pig = Pig(10,10,0)

# create boids at random positions
for i in range(numBoids):
    boid = Boid(random.randint(0, width), random.randint(0, height))
    boids.append(boid)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == KEYDOWN :
          # print event.key
          decX = 20 if event.key in [257, 260, 263] else 0
          incX = 20 if event.key in [259, 262, 265] else 0
          decY = 20 if event.key in [263, 264, 265] else 0
          incY = 20 if event.key in [257, 258, 259] else 0
          if event.key == K_SPACE :
              followPlayer = not followPlayer

          pig.rect.x += incX - decX
          pig.rect.y += incY - decY

          pigRect = pygame.Rect(pig.rect)
          pigRect.x = pig.rect.x
          pigRect.y = pig.rect.y

    for boid in boids:
        closeBoids = []
        for otherBoid in boids:
            if otherBoid == boid: continue
            distance = boid.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)

        boid.moveCloser(closeBoids)
        if followPlayer :
            boid.moveCloserPlayer(pig.rect)
        #boid.move = "MOVINGCLOSER"
        boid.moveWith(closeBoids)
        #boid.move = "MOVEWITH"
        boid.moveAway(closeBoids, 20)
        #boid.move = "MOVEAWAY"

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        border = 25
        if boid.x < border and boid.velocityX < 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.x > width - border and boid.velocityX > 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.y < border and boid.velocityY < 0:
            boid.velocityY = -boid.velocityY * random.random()
        if boid.y > height - border and boid.velocityY > 0:
            boid.velocityY = -boid.velocityY * random.random()
            
        boid.move()
        
    #screen.fill(black)
    screen.blit(fond, (0, 0))
    for boid in boids:
        boidRect = pygame.Rect(boid.rect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(boid.image, boidRect)

    screen.blit(pig.image, pig.rect)

    afficher_murs()

    pygame.display.flip()
    pygame.time.delay(10)
