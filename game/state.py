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
                return True
            case Quit():
                raise SystemExit
        return False
    def _render(self):
        if self.parent:
            self.parent._render()
        self.render()
    def render(self):
        pass
    def exit(self):
        if not self.parent:
            raise SystemExit
        g.state = self.parent
        return self.parent
    def on_enter(self):
        '''
        Special initialization function for... reasons.
        '''
        pass