import attrs
import numpy as np
from typing import Final


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


@attrs.define
class Graphic:
    ch: int
    fg: tuple[int, int, int]
    bg: tuple[int, int, int] = (0,0,0)


Name: Final = ('Name', str)
Description: Final = ('Description', str)

HP: Final = ('HP', int)


# Map

Tiles: Final = ('Tiles', np.ndarray)
MapShape: Final = ('MapShape', int)