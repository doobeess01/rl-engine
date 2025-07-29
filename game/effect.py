from tcod.ecs import Entity

class Effect:
    def __init__(self, entity: Entity, duration):
        self.entity = entity
        self.duration = duration
    def _affect(self):
        self.affect(self.entity)
        self.duration -= 1
        return self.duration
    def affect(self):
        pass
