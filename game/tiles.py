"""Tiles database."""

from __future__ import annotations

from typing import Final

import numpy as np
import tcod.console

TILES = np.asarray(
    [
        ("void", (ord(" "), (0, 0, 0), (0, 0, 0)), 0, True),
        ("wall", (ord("#"), (0,255,0), (0,0,0)), 0, False),
        ("window", (ord('#'), (255, 255, 255), (0, 0, 0)), 0, False),
        ("floor", (ord("."), (0,255,0), (0,0,0)), 1, True),
    ],
    dtype=[
        ("name", object),
        ("graphic", tcod.console.rgb_graphic),
        ("walk_cost", np.int8),
        ("transparent", np.bool),
    ],
)
TILES.flags.writeable = False
TILE_NAMES: Final = {tile["name"]: i for i, tile in enumerate(TILES)}