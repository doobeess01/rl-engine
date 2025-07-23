from pathlib import Path

import tcod

import g

from game.states import MainMenu
from game.controller import Controller


CONSOLE_WIDTH = 100
CONSOLE_HEIGHT = 64


THIS_DIR = Path(__file__, "..")
FONT = THIS_DIR / 'assets/Alloy_curses_12x12.png'


def main():
    g.console = tcod.console.Console(CONSOLE_WIDTH,CONSOLE_HEIGHT)
    tileset = tcod.tileset.load_tilesheet(FONT, 16, 16, tcod.tileset.CHARMAP_CP437)

    g.state = MainMenu()
    g.player = None

    with tcod.context.new(console=g.console, tileset=tileset) as g.context:
        while True:
            try:
                # If there is a queue, process other actors actions until the player is at the front of the queue
                while g.queue().front != g.player:
                    actor = g.queue().front
                    action = actor.components[Controller](actor)  # The AI chooses an action
                    action(actor)  # Execute chosen action
            except NameError:
                # If there is no queue, skip queue processing
                # Note: if there is no queue, there is no registry,
                #    and queue() accesses the registry, thus a NameError
                #    is thrown
                pass

            # Render
            g.console.clear()
            g.state._render()
            g.context.present(g.console)

            # Process player input
            for event in tcod.event.wait():
                g.state.on_event(event)


if __name__ == '__main__':
    main()