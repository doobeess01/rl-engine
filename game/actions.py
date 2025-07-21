import attrs

import g

from tcod.ecs import callbacks, Entity

from game.action import Action
from game.state import State

from game.world_tools import init_world

from game.tiles import TILES

from game.components import Position, Tiles, HP, Attack
from game.tags import IsActor, IsIn

from game.entity_tools import kill


# GAME ACTIONS

class Wait(Action):
    def __init__(self):
        super().__init__(cost=100)

@attrs.define
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
        self.target.components[HP] -= actor.components[Attack]


@callbacks.register_component_changed(component=HP)
def on_hp_change(entity: Entity, old: int | None, new: int | None):
    if new is not None:
        if new < 1:
            kill(entity)


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
        super().__init__()
        self.state = state

class ChangeState(StateAction):
    def execute(self, actor):
        g.state = self.state

class BeginGame(StateAction):
    def execute(self, actor):
        init_world()
        ChangeState(self.state)(actor)

class EnterSubstate(StateAction):
    def execute(self, actor):
        parent = g.state
        g.state = self.state
        g.state.parent = parent


# OTHER ACTIONS

class QuitGame(Action):
    def execute(self, actor):
        raise SystemExit