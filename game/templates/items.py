import g

from game.components import Name, Graphic, Description
from game.tags import IsStackable


def new_item(
        name: str = 'unknown creature', 
        graphic: Graphic = None, 
        desc: str = "[No description]", 
        stackable: bool = True,
        components: dict = {}, 
        tags: set = {},
        ):
    item = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc}|components,
        tags = tags
    )
    if stackable:
        item.tags.add(IsStackable)

    return item


POTION = new_item(
    name = 'potion',
    graphic = Graphic(ord('!'), (100,100,255),(0,0,0)),
    desc = 'A potion',
)