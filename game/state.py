from tcod.event import KeyDown, Quit

import g

from game.action import Action

class State:
    def __init__(self, keybindings={int: Action}, parent=None):
        assert isinstance(parent, self.__class__) or parent is None
        self.parent = parent
        self.keybindings = keybindings
    def on_event(self, event):
        match event:
            case KeyDown(sym=sym) if sym in self.keybindings:
                action = self.keybindings[sym]
                action(g.player)
            case Quit():
                raise SystemExit
    def render(self):
        pass
    def exit(self):
        if not self.parent:
            raise SystemExit
        return self.parent