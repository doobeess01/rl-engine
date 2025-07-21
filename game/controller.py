from tcod.ecs import Entity

from game.actions import Wait

class Controller:
    def __call__(self, actor):
        return Wait()
