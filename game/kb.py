'''State keybindings.'''


from tcod.event import KeySym as K, Modifier as M

from game.actions import CursorMove, Select

MENU = {
    K.UP: CursorMove(-1),
    K.DOWN: CursorMove(1),
    K.RETURN: Select(),
}