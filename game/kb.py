'''State keybindings.'''


from tcod.event import KeySym as K, Modifier as M

from game.actions import CursorMove, Select, Wait

MENU = {
    K.UP: CursorMove(-1),
    K.DOWN: CursorMove(1),
    K.RETURN: Select(),
}

IN_GAME = {
    K.PERIOD: Wait(),
    K.N5: Wait(),
}