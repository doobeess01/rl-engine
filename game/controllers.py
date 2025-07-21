import random

from game.controller import Controller
from game.actions import Bump

class Wander(Controller):
    def __call__(self, actor):
        d = (0,0)
        while d == (0,0):
            d = (random.randint(-1,1), random.randint(-1,1))
        return Bump(d)