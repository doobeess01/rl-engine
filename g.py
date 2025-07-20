import tcod
import tcod.ecs

import game.queue

console: tcod.console.Console
context: tcod.context.Context

registry: tcod.ecs.Registry
player: tcod.ecs.Entity

queue: game.queue.Queue

templates: dict[str: tcod.ecs.Entity]