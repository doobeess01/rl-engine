'''Base action class'''

from tcod.ecs import Entity
import g


class InvalidActionError(Exception):
    def __init__(self, action: str):
        n = 'n' if action[0] in 'aeiou' else ''
        super().__init__(f'Attempted to execute a{n} {action} action in an invalid state ({g.state.__class__.__name__})!')


class Action:
    def __init__(self, cost=-1):
        self.cost = cost
    def __call__(self, actor):
        self.execute(actor)
        if self.cost > -1:
            g.queue().move_front(self.cost)

    def execute(self, actor: Entity):
        pass
    def invalid_action_error(self):
        raise InvalidActionError(self.__class__.__name__)


class Pass(Action):
    '''Do nothing. Has the same purpose as the pass keyword.'''
    def __init__(self, *args):
        super().__init__()
    def execute(self, actor):
        pass