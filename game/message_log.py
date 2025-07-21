import attrs

import tcod.console

import g
from game.components import Position

@attrs.define
class Message:
    text: str
    fg: tuple[int,int,int]
    bg: tuple[int,int,int]

class MessageLog:
    def __init__(self, width=None):
        self.width = width
        assert width > 3
        self.messages = []
    def log(self, text: str, fg: tuple[int, int, int] = (255,255,255), bg: tuple[int, int, int] = (0,0,0)):
        self.messages.append((Message(text, fg, bg)))
    def render(self, position: Position, rows: int):
        for i, message in enumerate(self.messages[-rows:]):
            g.console.print(x=position.x, y=position.y+i, text=message.text, fg=message.fg, bg=message.bg)
    def clear(self):
        self.messages = []

def log(text: str, fg=(255,255,255), bg=(0,0,0)):
    '''Wrapper function for ease of use when interacting with the message log.'''
    g.registry[None].components[MessageLog].log(text, fg=fg, bg=bg)