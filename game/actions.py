import g
from game.action import Action


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


