from tcod.ecs import Entity

class QueueError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Queue:
    def __init__(self, inital_state: dict[int:list[Entity]]={}):
        self.queue = inital_state

    @property
    def front(self):
        return self.queue[min(self.queue)][0]
    
    def move_front(self, cost):
        try:
            self.queue[min(self.queue)+cost].append(self.front)
        except KeyError:
            self.queue[min(self.queue)+cost] = [self.front]
        del self.queue[min(self.queue)][0]
        if not len(self.queue[min(self.queue)]):
            del self.queue[min(self.queue)]
    
    def add(self, actor):
        if self.queue:
            self.queue[min(self.queue)].append(actor)
        else:
            self.queue[0] = [actor]

    def remove(self, actor):
        for position in self.queue:
            if self.queue[position] == actor:
                del self.queue[position]
                return
        raise QueueError('Tried to remove a nonexistent actor')

    def clear(self):
        self.queue = {}