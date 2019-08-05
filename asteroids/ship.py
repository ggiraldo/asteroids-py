# Asteroids Game
# Spatial ship class

import math
import pygame

from . import particle
from . import vector


class Ship():
    """ Space ship class definition """

    def __init__(self, x, y):

        self.particle = particle.Particle()
        self.particle.pos.x = x
        self.particle.pos.y = y
        self.theta = math.pi / 2
        self.omega = 0.
        self.r = 20

        # Dynamics parameters
        self.thrustForce = 0.3
        self.rotationalTorque = 0.01
        self.rotationalDamp = 0.8
        self.velocityDamp = 0.95

    def render(self, screen):
        """ Render using pygame"""        
        # Vertices in LCS
        x1 = self.r
        y1 = 0
        x2 = -0.7*self.r
        y2 = 0.7*self.r
        x3 = -0.7*self.r
        y3 = -0.7*self.r

        # Rotation
        s = math.sin(self.theta)
        c = math.cos(self.theta)

        (x1, y1) = (x1*c - y1*s, x1*s + y1*c) 
        (x2, y2) = (x2*c - y2*s, x2*s + y2*c) 
        (x3, y3) = (x3*c - y3*s, x3*s + y3*c) 

        # Translation
        x0 = self.particle.pos.x
        y0 = self.particle.pos.y
        x1 += x0
        y1 += y0
        x2 += x0
        y2 += y0
        x3 += x0
        y3 += y0
        
        points = ((x1,y1), (x2,y2), (x3,y3))

        # Actual drawing
        pygame.draw.polygon(screen, (230, 230, 230), points)

    def update(self, width, height):
        """ Update state """
        self.particle.update()
        self.particle.vel.mult(self.velocityDamp)
        self.particle.edges(width, height)
        self.theta += self.omega
        self.omega *= self.rotationalDamp

    def turn(self, factor):
        """ Turn ship """
        # Rotation is controlled with rotational acceleration
        self.omega += self.rotationalTorque * factor

    def thrust(self, factor):
        """ Trust ship """
        # Movement is controlled with acceleration
        thrustVector = vector.fromAngle(self.theta)
        thrustVector.setMag(self.thrustForce * factor)
        self.particle.applyForce(thrustVector)

    def hit(self, asteroid):
        """ Collision detection """
        r = vector.sub(self.particle.pos, asteroid.particle.pos)
        tol = 4 # Collision tollerance
        return  self.r + asteroid.r - r.mag() > tol
