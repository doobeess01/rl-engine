'''Base action class'''

from tcod.ecs import Entity
import g

class InvalidActionError(Exception):
    def __init__(self, action):
        super().__init__(f'Attempted to execute a {action} action in an invalid state!')


class Action:
    def __init__(self, cost=-1):
        self.cost = cost
    def __call__(self, actor):
        self.execute(actor)
        if self.cost > -1:
            g.queue.move_front(actor)

    def execute(self, actor: Entity):
        pass
    def invalid_action_error(self):
        raise InvalidActionError(self.__name__)


class Pass(Action):
    '''Do nothing. Has the same purpose as the pass keyword.'''

    def execute(self):
        pass