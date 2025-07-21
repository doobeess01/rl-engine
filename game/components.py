import attrs
import numpy as np
from typing import Final

from tcod.ecs import callbacks, Entity


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

@callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    '''Aesthetically pleasing means of finding entity at any given coordinate.'''
    if old == new:
        return
    if old:
        entity.tags.remove(old)
    if new:
        entity.tags.add(new)


@attrs.define
class Graphic:
    ch: int
    fg: tuple[int, int, int]
    bg: tuple[int, int, int] = (0,0,0)


Name: Final = ('Name', str)
Description: Final = ('Description', str)

HP: Final = ('HP', int)

Attack: Final = ('Attack', int)

# Map

Tiles: Final = ('Tiles', np.ndarray)
MapShape: Final = ('MapShape', int)