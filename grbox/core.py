
from pygame.sprite import Group

class Manager:
    def __init__(self):
        self.stack = []

    def top(self):
        return self.stack[-1] if self.stack else None

    def push(self, scene):
        scene.set_manager(self)
        self.stack.append(scene)

    def pop(self):
        last_scene = self.top()

        if last_scene:
            del self.stack[-1]

        return last_scene

class Scene(Group):
    def __init__(self):
        Group.__init__(self)

        self.manager = None
        self.initialize()

    def set_manager(self, manager):
        self.manager = manager

    def initialize(self):
        return NotImplemented

    def tick(self):
        return NotImplemented

    def move_west(self, down):
        return NotImplemented

    def move_east(self, down):
        return NotImplemented

    def move_both(self):
        return NotImplemented

