from tcod.event import KeySym as K

import g

from game.state import State

from game.action import Action, Pass
from game.actions import *

from game.message_log import MessageLog

from game.tiles import TILES

from game.entity_tools import inventory, add_to_inventory, drop

from game.tags import IsIn, IsActor
from game.components import Position, Graphic, Name, MapShape, Tiles, Quantity, ItemCategory, ITEM_CATEGORIES


# Actions (that require reference to states.py states)

class PickupItems(Action):
    def execute(self, actor: Entity):
        items = inventory(actor.relation_tag[IsIn], components=[Quantity], tags=[actor.components[Position]])
        if len(items) > 1:
            EnterSubstate(PickupItemMenu(items))
        elif len(items) > 0:
            PickupItem(items[0])(actor)
        else:
            log('There is nothing here to pick up.', colors=((200,200,200), (0,0,0)))


class Menu(State):
    '''Basic 1D menu state with no rendering.'''
    def __init__(self, options: list[tuple[str: Action]], cursor_start = 0):
        self.cursor = cursor_start
        self.options = options

        MENU = {
            K.UP: CursorMove(-1),
            K.DOWN: CursorMove(1),
            K.RETURN: Select(),
        }

        super().__init__(keybindings=MENU)
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

            K.I: EnterSubstate(InventoryView()),
            K.COMMA: PickupItems(),
            K.D: EnterSubstate(DropItemMenu()),
        }
        super().__init__(keybindings=IN_GAME)
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


class ToggleCategoryVisibility(Action):
    def __init__(self, category: int):
        self.category = category
        super().__init__()
    def execute(self, actor):
        try:
            g.state.shown_categories[self.category] = not g.state.shown_categories[self.category]  # Toggle
            g.state.on_enter()
        except AttributeError:
            self.invalid_action_error()


class ItemList(Menu):
    def __init__(self, action: Action, title: str, items: list, no_item_text: str = '[no items]'):
        self.action = action
        self.items = items
        self.shown_categories = {category: True for category in ITEM_CATEGORIES}
        super().__init__([])

    def on_enter(self):
        options = []
        sorted_inventory = {}
        for item in self.items:
            if sorted_inventory.get(item.components[ItemCategory], 0):
                sorted_inventory[item.components[ItemCategory]].append(item)
            else:
                sorted_inventory[item.components[ItemCategory]] = [item]
        for category in ITEM_CATEGORIES:
            if category in sorted_inventory:
                options.append((ITEM_CATEGORIES[category], ToggleCategoryVisibility(category)))
                for item in sorted_inventory.get(category, []) if self.shown_categories[category] else []:
                    options.append((item.components[Name], self.action(item)))

        self.options = options

    def render(self):
        if self.items:
            g.console.draw_frame(
                5,5,
                max([len(option[0]) for option in self.options])+(5*(max([item.components[Quantity] for item in self.items])>1))+4,len(self.options)+4,
                fg=(255,255,255),bg=(0,0,0)
            )
            g.console.print(6,6,'Inventory')
            item_index = 0
            for i,option in enumerate(self.options):
                indent = 3
                if isinstance(option[1], ToggleCategoryVisibility):
                    indent = 0
                    multiple_text = ''
                else:
                    quantity = self.items[item_index].components[Quantity]
                    multiple_text = f' (x{str(quantity)})' if quantity > 1 else ''
                    item_index += 1
                color = ((255,255,255),(0,0,0))
                if i == self.cursor:
                    color = ((0,0,0),(255,255,255))
                g.console.print(6+indent,8+i, option[0]+multiple_text, fg=color[0], bg=color[1])
        else:
            text = 'You are carrying nothing.'
            g.console.draw_frame(5,5,len(text)+2,3,fg=(255,255,255),bg=(0,0,0))
            g.console.print(6,6,text)


class InventoryView(ItemList):
    def __init__(self):
        super().__init__(Pass, 'Inventory', [], no_item_text='You are carrying nothing.')
    def on_enter(self):
        self.items = inventory(g.player)
        super().on_enter()


class PickupItemMenu(ItemList):
    def __init__(self, items):
        super().__init__(PickupItem, 'Pick up which?', items, no_item_text='THIS IS A BUG, please report it')

class DropItemMenu(ItemList):
    def __init__(self):
        super().__init__(DropItem, 'Drop which?', [], no_item_text='You are carrying nothing.')
    def on_enter(self):
        self.items = inventory(g.player)
        super().on_enter()


MAIN_MENU_OPTIONS = [('Play', BeginGame(InGame())), ('Achievements', Pass()), ('Quit', QuitGame()),]


# Main menu config (move to JSON or something?)

MAIN_MENU_TITLE = 'UNTITLED RL'
MAIN_MENU_TITLE_POSITION = (2,2)

MAIN_MENU_OPTIONS_OFFSET = (3,9)
MAIN_MENU_OPTIONS_STEP = 2
MAIN_MENU_CURSOR = '> '