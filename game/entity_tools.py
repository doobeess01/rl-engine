from tcod.ecs import Entity

import g
from game.components import Position, Name
from game.tags import IsActor, IsIn

from game.message_log import log
import game.msg as msg


def spawn_entity(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}) -> Entity:
    entity = template.instantiate()
    entity.components |= {Position: position}|components
    entity.tags |= tags
    entity.relation_tag[IsIn] = map_

    return entity


def spawn_creature(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}) -> Entity:
    creature = spawn_entity(template, map_, position=position, components=components, tags=tags)
    creature.tags.add(IsActor)
    return creature

def spawn_item(template: Entity, map_: Entity, position: Position = None, components: dict = {}, tags: set = {}) -> Entity:
    item = spawn_entity(template, map_, position=position, components=components, tags=tags)


def kill(actor: Entity):
    g.queue().remove(actor)
    log(f'{actor.components[Name]} dies!', fg=msg.DEATH) # message log 'entity died!'
    actor.clear()