from tcod.ecs import Entity

import numpy as np

import g
from game.components import Tiles, MapShape

from game.tiles import TILE_NAMES

def generate_level(shape: tuple[int, int]) -> Entity:
    map_ = g.registry.new_entity()
    map_.components[MapShape] = shape

    width = shape[0]
    height = shape[1]

    # Setup map components
    map_.components[Tiles] = np.full(shape, TILE_NAMES['wall'])

    map_.components[Tiles][1:width-1, 1:height-1] = np.full((width-2, height-2), TILE_NAMES['floor'])
    print(len(map_.components[Tiles][0]))

    return map_