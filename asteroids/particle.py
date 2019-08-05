# Asteroids Game
# Physics particle class

import pygame

from . import vector


class Particle():
    """ Physics 2D particle class definition """

    def __init__(self, x = 0, y = 0):
        """ Class constructor """
        self.pos = vector.Vector()
        self.pos.x = x
        self.pos.y = y
        self.vel = vector.Vector()
        self.acc = vector.Vector()

    def update(self):
        """ Physics update routine """
        self.vel.add(self.acc)
        self.pos.add(self.vel)

        self.acc.mult(0.0)

    def applyForce(self, f):
        """ Force applied to particle """
        self.acc.add(f)

    def render(self, screen, color=(255, 255, 255)):
        """ Render point """
        center = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, color, center, 2)

    def edges(self, width, height):
        """ Warp particle around screen """
        if(self.pos.x > width):
            self.pos.x = 0

        if(self.pos.x < 0):
            self.pos.x = width

        if(self.pos.y > height):
            self.pos.y = 0

        if(self.pos.y < 0):
            self.pos.y = height
