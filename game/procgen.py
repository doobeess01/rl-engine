from tcod.ecs import Entity

import numpy as np

import g
from game.components import Tiles, MapShape

from game.tiles import TILE_NAMES

def generate_level(width: int, height: int) -> Entity:
    map_ = g.registry.new_entity()
    map_.components[Tiles] = np.full((width, height), TILE_NAMES['wall'])
    map_.components[Tiles][1:width-1, 1:height-1] = TILE_NAMES['floor']
    map_.components[MapShape] = (width, height)
    return map_