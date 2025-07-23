from tcod.ecs import Entity

class QueueError(Exception):
    def __init__(self, message):
        super().__init__(message)


class QueueError(Exception):
    pass

class Queue:
    def __init__(self):
        self.queue = {}
    
    @property
    def front(self):
        return self.queue[min(self.queue)][0]
    
    def move_front(self, time_spent):
        chronoposition = time_spent + min(self.queue) # 8)
        try:
            self.queue[chronoposition].append(self.front)
        except KeyError:
            self.queue[chronoposition] = [self.front]
        del self.queue[min(self.queue)][0]  # Not using the function here because I'm not sure it will work properly
        if not self.queue[min(self.queue)]:
            del self.queue[min(self.queue)]

    def add(self, entity):
        try:
            self.queue[min(self.queue)].append(entity)
        except ValueError:
            self.queue[0] = [entity]

    def remove(self, actor: Entity):
        for chronoposition in self.queue:
            if actor in self.queue[chronoposition]:
                self.queue[chronoposition].remove(actor)
                return
        raise QueueError('')
    
    def clear(self):
        self.queue = {}