from tcod.ecs import callbacks, Entity

from game.components  import Position, HP, Effects
from game.entity_tools import kill


@callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    '''Aesthetically pleasing means of finding entity at any given coordinate.'''
    if old == new:
        return
    if old:
        entity.tags.remove(old)
    if new:
        entity.tags.add(new)

@callbacks.register_component_changed(component=HP)
def on_hp_change(entity: Entity, old: int | None, new: int | None):
    if new is not None:
        if new < 1:
            kill(entity)

@callbacks.register_component_changed(component=int)
def on_time_advance(entity: Entity, old: int | None, new: int | None):
    '''Handle things like effects (healing, poisoned, etc.), fire, etc.'''

    for actor in entity.registry.Q.all_of(components=[Effects]):
        new_effects = []
        for effect in actor.components[Effects]:
            if effect._affect(actor):
                new_effects.append(effect)
        actor.components[Effects] = new_effects