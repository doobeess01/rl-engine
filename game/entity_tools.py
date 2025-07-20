from tcod.ecs import Entity

import g
from game.components import Position
from game.tags import IsIn


def spawn_entity(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}):
    entity = template.instantiate()
    entity.components |= {Position: position}|components
    entity.tags |= tags
    entity.relation_tag[IsIn] = map_

    return entity


# TODO: Assess if the two below functions are actually needed

def spawn_creature(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}):
    creature = spawn_entity(template, map_, position=position, components=components, tags=tags)
    return creature

def spawn_item(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}):
    item = spawn_entity(template, map_, position=position, components=components, tags=tags)