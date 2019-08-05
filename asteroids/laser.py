# Asteroids Game
# Laser class definition

import pygame 

from . import particle
from . import vector

class Laser():
    """ Laser class definition """

    def __init__(self, x, y, theta):
        """ Class constructor """

        self.particle = particle.Particle()
        self.particle.pos.x = x
        self.particle.pos.y = y
        self.particle.vel = vector.fromAngle(theta)
        self.particle.vel.setMag(10.0)

    def update(self):
        """ Physics update """
        self.particle.update()

    def render(self, screen):
        """ Draw laser on screen """
        self.particle.render(screen, (255, 255, 0))

    def hit(self, asteroid):
        """ Collision detection with asteroid """
        r = vector.sub(self.particle.pos, asteroid.particle.pos)
        return r.mag() < asteroid.r
