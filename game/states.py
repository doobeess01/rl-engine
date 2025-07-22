import g

import game.kb as kb
from game.state import State

from game.action import Action, Pass
from game.actions import BeginGame, QuitGame

from game.message_log import MessageLog

from game.tiles import TILES

from game.tags import IsIn, IsActor
from game.components import Position, Graphic, MapShape, Tiles, Quantity

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
        self.options[self.cursor][1](g.player)


class MainMenu(Menu):
    def __init__(self):
        super().__init__(MAIN_MENU_OPTIONS)
    def render(self):
        g.console.draw_frame(0,0,g.console.width,g.console.height,fg=(255,0,0))
        g.console.print(*MAIN_MENU_TITLE_POSITION, MAIN_MENU_TITLE)
        for i,option in enumerate(self.options):
            cursor_text = MAIN_MENU_CURSOR if i==self.cursor else ''
            g.console.print(MAIN_MENU_OPTIONS_OFFSET[0],MAIN_MENU_OPTIONS_OFFSET[1]+(MAIN_MENU_OPTIONS_STEP*i),cursor_text+option[0])


class InGame(State):
    def __init__(self):
        super().__init__(keybindings=kb.IN_GAME)
    def render(self):
        map_ = g.player.relation_tag[IsIn]
        g.console.rgb[0:map_.components[MapShape][0], 0:map_.components[MapShape][1]] = TILES['graphic'][map_.components[Tiles]]
    
        rendered_priority: dict[Position, int] = {}
        for entity in g.registry.Q.all_of(components=[Position, Graphic], relations=[(IsIn, map_)]):
            pos = entity.components[Position]
            if not (0 <= pos.x < g.console.width and 0 <= pos.y < g.console.height):
                continue  # Out of bounds
            render_order = 1
            if Quantity in entity.components:
                render_order = 2
            if IsActor in entity.tags:
                render_order = 3
            if g.player == entity:
                render_order = 4
            if rendered_priority.get(pos, 0) >= render_order:
                continue  # Do not render over a more important entity
            rendered_priority[pos] = render_order
            graphic = entity.components[Graphic]
            g.console.rgb[["ch", "fg"]][pos.ij] = graphic.ch, graphic.fg

        g.registry[None].components[MessageLog].render(Position(0,56),7)


MAIN_MENU_OPTIONS = [('Play', BeginGame(InGame())), ('Achievements', Pass()), ('Quit', QuitGame()),]

# Main menu config (move to JSON or something?)

MAIN_MENU_TITLE = 'UNTITLED RL'
MAIN_MENU_TITLE_POSITION = (2,2)

MAIN_MENU_OPTIONS_OFFSET = (3,9)
MAIN_MENU_OPTIONS_STEP = 2
MAIN_MENU_CURSOR = '> '