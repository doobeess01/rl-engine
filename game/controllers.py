import random

from game.controller import Controller
from game.actions import Bump

class Wander(Controller):
    def choose_action(self):
        return Bump((random.randint(-1,1), random.randint(-1,1)))