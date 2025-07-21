import attrs

import tcod.console

import g
from game.components import Position

@attrs.define
class Message:
    text: str
    fg: tuple[int,int,int]
    bg: tuple[int,int,int]
    count: int = 1

    def __eq__(self, other):
        if self.text == other.text and self.fg == other.fg and self.bg == other.bg:
            return True
        return False


class MessageLog:
    def __init__(self, width=None):
        self.width = width
        self.messages = []
    def log(self, text: str, fg: tuple[int, int, int] = (255,255,255), bg: tuple[int, int, int] = (0,0,0)):
        message = Message(text, fg, bg)
        try:
            if message == self.messages[-1]:
                self.messages[-1].count += 1
                return
        except IndexError:
            pass
        self.messages.append(message)
    def render(self, position: Position, rows: int):
        for i, message in enumerate(self.messages[-rows:]):
            multiple_text = f' (x{message.count})' if message.count > 1 else ''
            g.console.print(x=position.x, y=position.y+i, text=message.text + multiple_text, fg=message.fg, bg=message.bg)
    def clear(self):
        self.messages = []

def log(text: str, fg=(255,255,255), bg=(0,0,0)):
    '''Wrapper function for ease of use when interacting with the message log.'''
    g.registry[None].components[MessageLog].log(text, fg=fg, bg=bg)