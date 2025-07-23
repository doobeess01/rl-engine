from tcod.ecs import callbacks, Entity

from game.components  import Position, HP
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