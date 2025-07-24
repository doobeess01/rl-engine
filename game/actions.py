import copy

import g

from tcod.ecs import callbacks, Entity

from game.action import Action
from game.state import State

from game.world_tools import init_world

from game.message_log import log
import game.colors as colors

from game.tiles import TILES

from game.components import Position, Tiles, HP, Attack, Name, Quantity
from game.tags import IsActor, IsIn

from game.entity_tools import add_to_inventory, drop


# GAME ACTIONS

class Wait(Action):
    def __init__(self):
        super().__init__(cost=100)

class Bump(Action):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    def execute(self, actor):
        blocking_entities = [e for e in actor.registry.Q.all_of(tags=[IsActor, actor.components[Position]+self.direction])]
        if blocking_entities:
            Melee(blocking_entities[0])(actor)
        else:
            Move(self.direction)(actor)


class Move(Action):    
    def __init__(self, direction):
        self.direction = direction
        super().__init__(cost=100)

    def execute(self, actor):
        map_ = actor.relation_tag[IsIn]
        new_position = actor.components[Position] + self.direction
        if TILES['walk_cost'][map_.components[Tiles][new_position.ij]]>0:
            actor.components[Position] = new_position

class Melee(Action):
    def __init__(self, target):
        self.target = target
        super().__init__(cost=100)

    def execute(self, actor):
        damage = actor.components[Attack]
        colors = colors.MSG_ATTACK if actor != g.player else ((255,255,255),(0,0,0))
        log(f'{actor.components[Name]} attacks {self.target.components[Name]} for {damage} damage!', colors)
        self.target.components[HP] -= damage


class PickupItem(Action):
    def __init__(self, item):
        self.item = item
        super().__init__(cost=100)
    def execute(self, actor):
        log(f'You pick up the {self.item.components[Name]}.')
        add_to_inventory(self.item, actor)


class DropItem(Action):
    def __init__(self, item):
        self.item = item
        super().__init__(cost=100)
    def execute(self, actor):
        quantity = self.item.components[Quantity]
        log(f'You drop the {self.item.components[Name]}{" (x"+str(quantity)+")" if quantity > 1 else ""}.')
        drop(self.item)
        g.state.on_enter()


# UI ACTIONS

class CursorMove(Action):
    def __init__(self, direction: int):
        super().__init__()
        assert direction in (-1,1)
        self.direction = direction
    def execute(self, actor):
        try:
            g.state.move_cursor(self.direction)
        except AttributeError:
            self.invalid_action_error()

class Select(Action):
    def execute(self, actor):
        try:
            g.state.select()
        except AttributeError:
            self.invalid_action_error()


# STATE ACTIONS

class StateAction(Action):
    def __init__(self, state: State):
        self.state = copy.deepcopy(state)
        super().__init__()
        

class ChangeState(StateAction):
    def execute(self, actor):
        self.state.on_enter()
        g.state = self.state

class ExitState(Action):
    def execute(self, actor):
        g.state.exit()

class BeginGame(StateAction):
    def execute(self, actor):
        init_world()
        ChangeState(self.state)(actor)

class EnterSubstate(StateAction):
    def execute(self, actor):
        self.state.on_enter()
        parent = g.state
        g.state = self.state
        g.state.parent = parent

        from tcod.event import KeySym as K
        g.state.keybindings[K.ESCAPE] = ExitState()


# OTHER ACTIONS

class QuitGame(Action):
    def execute(self, actor):
        raise SystemExit