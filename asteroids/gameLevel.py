# Asteroids Game
# Game level class

import pygame
import pygame.freetype
from random import random

from . import ship
from . import asteroid
from . import laser

class GameLevel():
    """ Asteroids game level class definition """

    def __init__(self, level, width, height):
        """ Class constructor """
        self.level = level
        self.widht = width
        self.height = height

        # Initialize ship
        self.ship = ship.Ship(width / 2, height / 2)
        self.turn = 0
        self.thrust = 0

        # Initialize asteroids according to leve
        # Set initial speeds
        self.asteroids = []
        self.initialAsteroids = 3 + 2*self.level

        for i in range(self.initialAsteroids):
            
            self.asteroids.append(asteroid.Asteroid(self.widht, self.height))
            speed = 1.0 + random() * self.level / 5.0
            self.asteroids[i].particle.vel.mult(speed)

        # Initialize lasers
        self.lasers = []

        # Initialize game control variables
        self.score = 0
        self.gameOver = False
        self.levelCleared = False

        # Initialize font for rendering text
        self.font = pygame.freetype.Font(None, 20)

        # State for training
        self._asteroidDestroyed = False
        
    def update(self):
        """ Update physics routine """
        for asteroid in self.asteroids:
            asteroid.update(self.widht, self.height)

        for laser in self.lasers:
            laser.update()

        self.ship.turn(self.turn)
        self.ship.thrust(self.thrust)
        self.ship.update(self.widht, self.height)

        self.laserCollision()
        self.shipCollision()

        if(len(self.asteroids) == 0):
            print('LEVEL {} CLEARED'.format(self.level))
            self.levelCleared = True

    def render(self, screen):
        """ Render using pygame routines """
        for asteroid in self.asteroids:
            asteroid.render(screen)

        for laser in self.lasers:
            laser.render(screen)

        self.ship.render(screen)

    def renderHUD(self, screen):
        """ Render game state info in screen """
        self.font.render_to(screen, (20, 20), 'LEVEL: {}'.format(self.level), (255, 255, 255))
        self.font.render_to(screen, (self.widht - 160, 20), 'SCORE: {}'.format(self.score), (255, 255, 255))
        self.font.render_to(screen, (20, self.height - 70), 'HELP:', (255, 255, 255), size=15)
        self.font.render_to(screen, (20, self.height - 50), 'WASD TO MOVE,', (255, 255, 255), size=15)
        self.font.render_to(screen, (20, self.height - 30), 'SPACEBAR TO FIRE.', (255, 255, 255), size=15)
        if self.gameOver:
            self.font.render_to(screen, (self.widht / 2 - 60, self.height / 2), 'GAME OVER', (0, 128, 0))
            self.font.render_to(screen, (self.widht / 2 - 120, self.height / 2 + 30), 'PRESS FIRE TO RESTART', (0, 128, 0))

    def laserCollision(self):
        """ Check for collision between lasers and asteroids"""
        # Check lasers leaving screen
        for laser in self.lasers[:]:
            if(laser.particle.pos.x < 0 or
               laser.particle.pos.x > self.widht or
               laser.particle.pos.y < 0 or
               laser.particle.pos.y > self.height):
                 self.lasers.remove(laser)
                 continue
        
        # Check laser-asteroid collisions
        for laser in self.lasers[:]:
            for asteroid in self.asteroids[:]:
                if laser.hit(asteroid):
                    self.score += 100 - asteroid.r
                    print("Score: ", self.score)
                    childs = asteroid.split()
                    if len(childs) > 0:
                        self.asteroids.append(childs[0])
                        self.asteroids.append(childs[1])
                    self.asteroids.remove(asteroid)
                    self.lasers.remove(laser)
                    self._asteroidDestroyed = True
                    break

    def shipCollision(self):
        """ Check for collision between ship and asteroids"""
        for asteroid in self.asteroids:
            if(self.ship.hit(asteroid)):
                # Game Over
                print('GAME OVER')
                self.gameOver = True

    def fire(self):
        """ Fire laser """
        l = laser.Laser(self.ship.particle.pos.x,
                        self.ship.particle.pos.y,
                        self.ship.theta)
        self.lasers.append(l)

    def keyPressed(self, symbol):
        """ Key control """
        if symbol == pygame.K_d:
            self.turn = 1
        if symbol == pygame.K_a:
            self.turn = -1
        if symbol == pygame.K_w:
            self.thrust = 1
        if symbol == pygame.K_s:
            self.thrust = -1
        if symbol == pygame.K_SPACE:
            self.fire()

    def keyReleased(self):
        """ Control key released """
        self.turn = 0
        self.thrust = 0

    def asteroidDestroyed(self):
        """ Return True if an asteroid was recently destroyed """
        if self._asteroidDestroyed:
            self._asteroidDestroyed = False
            return True
        else:
            return False
        