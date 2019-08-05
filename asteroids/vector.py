# Asteroids Game
# 2D vector class and related functions

from random import random as rnd
from math import sin, cos

class Vector():
    """ 2D vector """

    def __init__(self, x = 0, y = 0):
        """ Class constructor """
        self.x = x
        self.y = y

    def mag(self):
        """ Vector magnitude """
        return (self.x**2 + self.y**2) ** 0.5

    def mult(self, f):
        """ Multiply vector by a scalar """
        self.x *= f
        self.y *= f
        return self

    def setMag(self, r):
        """ Change vector magnitude preserving orientation """
        r0 = self.mag()
        self.mult( r / r0 )

    def add(self, v):
        """" Add vector """
        self.x += v.x
        self.y += v.y


def sub(a, b):
    """ Vector subtraction """
    return Vector(a.x - b.x, a.y - b.y)


def random():
    """ Create random vector """
    return Vector(rnd(), rnd())


def fromAngle(theta):
    """ Create vector from angle orientation """
    x = cos(theta)
    y = sin(theta)
    return Vector(x, y)
