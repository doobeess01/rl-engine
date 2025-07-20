import g

from game.components import Name, Graphic, Description, HP


def new_creature(
        name: str = 'unknown creature', 
        graphic: Graphic = None, 
        desc: str = "[No description]", 
        hp: int = 10, 
        components: dict = {}, 
        tags: set = {},
        ):
    entity = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc, HP: hp,}|components,
        tags = tags
    )
    g.templates[name] = entity


def init_creatures():
    new_creature(
        name='player',
        graphic=Graphic(ord('@'), (255,255,255), (0,0,0)),
        desc="You're you.",
        hp=15,
    )