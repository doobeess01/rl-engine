import tcod.ecs

import g

from game.queue import Queue
from game.procgen import generate_level

from game.tags import IsIn

def init_world():
    g.registry = tcod.ecs.Registry()
    g.queue = Queue()

    g.player = g.registry.new_entity()

    map_ = generate_level(20,20)
    g.player.relation_tag[IsIn] = map_
    enter_level(map_)


def enter_level(map_):
    g.queue.clear()
    g.queue.add(g.player)
    for entity in g.registry.Q.all_of(relations=[(IsIn, map_)]):
        g.queue.add(entity)