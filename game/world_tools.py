import tcod.ecs

import g

from game.queue import Queue
from game.message_log import MessageLog
from game.procgen import generate_level
from game.entity_tools import spawn_creature, spawn_item, add_to_inventory

from game.components import Position
from game.tags import IsIn, IsActor


def init_world():
    g.registry = tcod.ecs.Registry()

    g.templates = {}

    g.registry[None].components[Queue] = Queue()
    g.registry[None].components[MessageLog] = MessageLog(width=20)

    map_ = generate_level((55,80))

    from game.templates.creatures import PLAYER, MONSTER
    from game.templates.items import POTION, SWORD
      # Can't be imported earlier because of when the registry is initialized
    g.player = spawn_creature(PLAYER, map_, position=Position(1,1))
    spawn_creature(MONSTER, map_, position=Position(5,5))
    spawn_creature(MONSTER, map_, position=Position(15,5))
    spawn_creature(MONSTER, map_, position=Position(15,15))

    spawn_item(POTION, map_, position=Position(2,2))
    player_weapon = spawn_item(SWORD, map_, position=Position(3,2))
    player_potion = spawn_item(POTION, map_, position=Position(3,2))
    add_to_inventory(player_potion, g.player)
    add_to_inventory(player_weapon, g.player)

    enter_level(map_)
    

def enter_level(map_):
    g.queue().clear()
    g.queue().add(g.player)
    for entity in g.registry.Q.all_of(relations=[(IsIn, map_)], tags=[IsActor]):
        if entity != g.player:
            g.queue().add(entity)