from tcod.ecs import Entity, IsA

import g
from game.components import Position, Name, Quantity
from game.tags import IsIn, IsActor, IsStackable

from game.message_log import log
import game.colors as colors


# Generic functions

def spawn_entity(template: Entity, map_: Entity, position: Position, components: dict = {}, tags: set = {}) -> Entity:
    entity = template.instantiate()
    entity.components |= {Position: position}|components
    entity.tags |= tags
    entity.relation_tag[IsIn] = map_

    return entity


# Creature functions

def spawn_creature(template: Entity, map_: Entity, position: Position, components: dict = {}, tags: set = {}) -> Entity:
    creature = spawn_entity(template, map_, position, components=components, tags=tags)
    creature.tags.add(IsActor)
    return creature

def kill(actor: Entity):
    g.queue().remove(actor)
    log(f'{actor.components[Name]} dies!', colors.MSG_DEATH)
    actor.clear()


# Item functions

def spawn_item(template: Entity, map_: Entity, position: Position, quantity: int = 1, components: dict = {}, tags: set = {}):
    for e in g.registry.Q.all_of(tags=[position, IsStackable], relations=[(IsIn, map_), (IsA, template)]):
        # If there is an identical stackable item on the same square, add to its quantity
        e.components[Quantity] += quantity
        return e
    else:
        item = spawn_entity(template, map_, position, components={Quantity: quantity}|components, tags=tags)
        return item


def inventory(entity: Entity, components: list = [], tags: list[str] = []):
    '''
    Return the inventory of an entity (all items with the IsIn relation to it)
    '''
    return [e for e in entity.registry.Q.all_of(relations=[(IsIn, entity)], components=components, tags=tags)]


def add_to_inventory(item: Entity, actor: Entity):
    '''
    Add an item to an entity's inventory. This modifies the entities' IsIn relation, meaning it will be removed from its previous location.
    '''
    stackable_inventory = inventory(actor, tags=[IsStackable])
    for other_item in stackable_inventory:
        if other_item.relation_tag[IsA] == item.relation_tag[IsA]:
            other_item.components[Quantity] += item.components[Quantity]
            item.clear()
            return
    item.relation_tag[IsIn] = actor
    del item.components[Position]

def drop(item: Entity):
    item.components[Position] = item.relation_tag[IsIn].components[Position]
    item.relation_tag[IsIn] = item.relation_tag[IsIn].relation_tag[IsIn]
    return item