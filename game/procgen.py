from tcod.ecs import Entity

import numpy as np

import g
from game.components import Tiles, MapShape

from game.tiles import TILE_NAMES

def generate_level(shape: tuple[int, int]) -> Entity:
    map_ = g.registry.new_entity()
    map_.components[MapShape] = shape

    height = shape[0]
    width = shape[1]

    # Setup map components
    map_.components[Tiles] = np.full(shape, TILE_NAMES['wall'])

    map_.components[Tiles][1:height-1, 1:width-1] = np.full((height-2, width-2), TILE_NAMES['floor'])
    map_.components[Tiles][3,1:width-1] = TILE_NAMES['window']

    return map_