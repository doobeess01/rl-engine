import tcod.ecs

import g

from game.queue import Queue
from game.procgen import generate_level
from game.entity_tools import spawn_creature

from game.components import Position
from game.tags import IsIn


def init_world():
    g.registry = tcod.ecs.Registry()

    g.templates = {}

    g.registry[None].components[Queue] = Queue()

    map_ = generate_level(20,20)

    from game.templates.creatures import PLAYER  # Can't be imported earlier because of when the registry is init
    g.player = spawn_creature(PLAYER, map_, Position(1,1))

    enter_level(map_)
    

def enter_level(map_):
    g.queue().clear()
    g.queue().add(g.player)
    for entity in g.registry.Q.all_of(relations=[(IsIn, map_)]):
        g.queue().add(entity)