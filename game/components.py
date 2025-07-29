import attrs
import numpy as np
from typing import Final

from tcod.ecs import callbacks, Entity

from game.effect import Effect


# General

@attrs.define
class Position:
    x: int
    y: int

    @property
    def ij(self):
        return self.y, self.x

    def __add__(self, other: tuple[int, int]):
        return self.__class__(self.x+other[0], self.y+other[1])

    def __hash__(self):
        return hash((self.x, self.y))


@attrs.define
class Graphic:
    ch: int
    fg: tuple[int, int, int]
    bg: tuple[int, int, int] = (0,0,0)


Name: Final = ('Name', str)
Description: Final = ('Description', str)
Effects: Final = ('Effects', list[Effect])

HP: Final = ('HP', int)
Attack: Final = ('Attack', int)

Quantity: Final = ('Quantity', int)

ItemCategory: Final = ('ItemCategory', int)

ITEM_CATEGORIES = {
    1: 'weapons',
    2: 'armor',
    3: 'scrolls',
    4: 'potions',
    5: 'staves',
}


# Map

Tiles: Final = ('Tiles', np.ndarray)
MapShape: Final = ('MapShape', int)