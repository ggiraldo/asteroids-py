# Asteroids Game
# Asteroid class definition

from random import randint, random
import math
import pygame

from . import particle
from . import vector


class Asteroid():
    """ Asteroid class definition """

    def __init__(self, width, height, x = None, y = None, r=None):
        """ Class constructor """
        self.rMin = 20
        self.rMax = 60
        self.r = r
        if self.r is None:
            self.r = randint(self.rMin, self.rMax)

        self.theta = 0.
        self.omegaMax = 0.05
        self.omega = self.omegaMax * (random() - 0.5) * 2.0

        self.width = width
        self.height = height

        self.particle = particle.Particle(width/2, height/2)

        # Avoid asteroids from spawning at center
        # So no initial collitions
        c = vector.Vector(width/2, height/2)
        d = vector.sub(c, self.particle.pos).mag()
        dMin = 2.0*(self.r + 50)

        if(x is not None and y is not None):
            # Case for given spawn position
            self.particle.pos.x = x
            self.particle.pos.y = y
        else:
            # Case for random initial position
            while(d < dMin):
                self.particle.pos.x = random() * width
                self.particle.pos.y = random() * height
                d = vector.sub(c, self.particle.pos).mag()

        self.particle.vel = vector.random()
        self.corners = randint(5, 9)

        self.radii = []
        for _ in range(self.corners):
            ri = randint(int(0.8*self.r), int(1.2*self.r))
            self.radii.append(ri)

    def update(self, width, height):
        """ Physics update routine """
        self.particle.update()
        self.particle.edges(width, height)
        self.theta += self.omega

    def render(self, screen):
        """ Draw asteroid on screen """
        # Vertices in LCS
        points = []
        for i in range(self.corners):
            angle = 2 * math.pi * i / self.corners
            radius = self.radii[i]
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append((x,y))
        
        # Rotation
        points_rot = []
        s = math.sin(self.theta)
        c = math.cos(self.theta)
        for p in points:
            x = p[0]
            y = p[1]
            (x, y) = (x*c - y*s, x*s + y*c)
            points_rot.append((x,y))

        # Translation
        points_trans = []
        for p in points_rot:
            x = p[0] + self.particle.pos.x
            y = p[1] + self.particle.pos.y
            points_trans.append((x,y))

        # Actual drawing
        pygame.draw.polygon(screen, (51, 51, 51), points_trans)
        pygame.draw.polygon(screen, (255, 255, 255), points_trans, 1)

    def split(self):
        """ Split asteroid when destroyed """
        childs = []
        rNew = self.r // 2
        vNew = self.particle.vel.mag() * 2.0

        if rNew > self.rMin :
            childs.append(Asteroid(self.width, self.height, self.particle.pos.x, self.particle.pos.y, rNew))
            childs.append(Asteroid(self.width, self.height, self.particle.pos.x, self.particle.pos.y, rNew))
            childs[0].particle.vel.setMag(vNew)
            childs[1].particle.vel.setMag(vNew)

        return childs
