import g

from game.action import Action
from game.state import State

from game.world_tools import init_world

# GAME ACTIONS

class Wait(Action):
    def __init__(self):
        super().__init__(cost=100)


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