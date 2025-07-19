import g

import game.kb as kb
from game.state import State
from game.action import Action, Pass

class Menu(State):
    '''Basic 1D menu state with no rendering.'''
    def __init__(self, options: list[tuple[str: Action]], cursor_start = 0):
        self.cursor = cursor_start
        self.options = options
        super().__init__(keybindings=kb.MENU)
    def move_cursor(self, step):
        self.cursor += step
        if self.cursor < 0:
            self.cursor = len(self.options) - 1
        elif self.cursor > len(self.options) - 1:
            self.cursor = 0
    def select(self):
        self.options[self.cursor][1].execute()


MAIN_MENU_OPTIONS = [('Play', Pass()), ('Achievements', Pass()), ('Quit', Pass()),]


# Main menu config (move to JSON or something?)

MAIN_MENU_TITLE = 'UNTITLED SURVIVAL GAME'
MAIN_MENU_TITLE_POSITION = ()

MAIN_MENU_OPTIONS_OFFSET = (3,9)
MAIN_MENU_OPTIONS_STEP = 2
MAIN_MENU_CURSOR = '> '


class MainMenu(Menu):
    def __init__(self):
        super().__init__(MAIN_MENU_OPTIONS)
    def render(self):
        g.console.draw_frame(0,0,g.console.width,g.console.height,fg=(255,0,0))
        for i,option in enumerate(self.options):
            cursor_text = MAIN_MENU_CURSOR if i==self.cursor else ''
            g.console.print(MAIN_MENU_OPTIONS_OFFSET[0],MAIN_MENU_OPTIONS_OFFSET[1]+(MAIN_MENU_OPTIONS_STEP*i),cursor_text+option[0])