from tcod.ecs import Entity

from game.actions import Wait

class Controller:
    def __init__(self, actor: Entity):
        self.actor = actor
    def choose_action(self, actor):
        return Wait()
