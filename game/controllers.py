import random

from game.controller import Controller
from game.actions import Bump, Wait
from game.tiles import TILES
from game.components import Position, Tiles
from game.tags import IsIn


class Wander(Controller):
    def __call__(self, actor):
        directions = [(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1)]
        map_ = actor.relation_tag[IsIn]
        while directions:
            direction = random.choice(directions)
            new_position = actor.components[Position] + direction
            if TILES['walk_cost'][map_.components[Tiles][new_position.ij]]>0:
                return Bump(direction)
        return Wait()