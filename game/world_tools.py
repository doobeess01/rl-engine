import tcod.ecs

import g

from game.procgen import generate_level

from game.tags import IsIn

def init_world():
    g.registry = tcod.ecs.Registry()
    g.player = g.registry.new_entity()

    map_ = generate_level(20,20)
    g.player.relation_tag[IsIn] = map_