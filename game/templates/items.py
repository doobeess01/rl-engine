import g

from game.components import Name, Graphic, Description, ItemCategory, ITEM_CATEGORIES
from game.tags import IsStackable


def new_item(
        name: str, 
        graphic: Graphic, 
        category: int,
        desc: str, 
        stackable: bool = True,
        components: dict = {}, 
        tags: set = {},
        ):
    item = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc, ItemCategory: category,}|components,
        tags = tags
    )
    if stackable:
        item.tags.add(IsStackable)

    return item


POTION = new_item(
    name = 'potion',
    graphic = Graphic(ord('!'), (100,100,255),(0,0,0)),
    desc = 'A potion',
    category = 4,
)