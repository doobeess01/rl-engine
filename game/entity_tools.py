from tcod.ecs import Entity

import g
from game.components import Position
from game.tags import IsIn


def spawn_creature(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}):
    entity = template.instantiate()
    entity.components |= {Position: position}|components
    entity.tags |= tags
    entity.relation_tag[IsIn] = map_


def spawn_item(template: Entity, position: Position = None, components: dict = {}, tags: set = {}):
    entity = template.instantiate()
    entity.components |= {Position: position}|components
    entity.tags |= tags