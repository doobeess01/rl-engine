import tcod
import tcod.ecs

from game.queue import Queue

console: tcod.console.Console
context: tcod.context.Context

registry: tcod.ecs.Registry
player: tcod.ecs.Entity

def queue():
    return registry[None].components[Queue]

templates: dict[str: tcod.ecs.Entity]