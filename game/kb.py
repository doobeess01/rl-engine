'''State keybindings.'''


from tcod.event import KeySym as K, Modifier as M

from game.actions import CursorMove, Select, Wait, Bump

MENU = {
    K.UP: CursorMove(-1),
    K.DOWN: CursorMove(1),
    K.RETURN: Select(),
}

IN_GAME = {
    # North
    K.UP: Bump((0,-1)),
    K.N8: Bump((0,-1)),

    # Northeast
    K.N9: Bump((1,-1)),

    # East
    K.RIGHT: Bump((1,0)),
    K.N6: Bump((1,0)),

    # Southeast
    K.N3: Bump((1,1)),

    # South
    K.DOWN: Bump((0,1)),
    K.N2: Bump((0,1)),

    # Southwest
    K.N1: Bump((-1,1)),

    # West
    K.LEFT: Bump((-1,0)),
    K.N4: Bump((-1,0)),

    # Northwest
    K.N7: Bump((-1,-1)),

    K.PERIOD: Wait(),
    K.N5: Wait(),
}