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

    return entity


PLAYER = new_creature(
    name='player',
    graphic=Graphic(ord('@'), (255,255,255), (0,0,0)),
    desc="You're you.",
    hp=15,
)

MONSTER = new_creature(
    name='monster',
    graphic=Graphic(ord('M'), (255,0,0), (0,0,0)),
    desc="It's a horrible monster!",
    hp=5,
)
