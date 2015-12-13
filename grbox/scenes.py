
from .core import Scene
from .sprites import HorizonLine, Box, Dialog, Fruit, RandomFruit

class GameScene(Scene):
    M_BOTH = 'both'
    M_WEST = 'west'
    M_EAST = 'east'

    def initialize(self):
        self.time = 0

        self.add(HorizonLine((0, 255, 0)))

        self.box = Box((255, 0, 255), 1)
        self.box_speed = 2

        self.dialog = Dialog(["What? I'm a box.",
                              "I'm very small.",
                              "I want to grow."])

        self.last_move = None
        self.down_count = 0

    def tick(self):
        self.time += 1

        if self.time == 6:
            self.add(Fruit('apple', Fruit.NORMAL, Fruit.VERTICAL, 320))
            self.dialog = Dialog(["Look! A giant apple!",
                                  "I want that."])
        if self.time == 9:
            self.dialog = None
        if self.time == 12:
            self.dialog = Dialog(["That was delicious.",
                                  "I want more."])
        if self.time == 14:
            self.add(Fruit('cherry', Fruit.NORMAL, Fruit.VERTICAL, 120))
            self.dialog = None
        if self.time == 16:
            self.add(Fruit('strawberry', Fruit.NORMAL, Fruit.VERTICAL, 520))
            self.dialog = Dialog(["Mmmh... Strawberry.",
                                  "But it seems too far.",
                                  "I need double-speed."])
        if self.time == 20:
            self.dialog = None
        if self.time == 22:
            self.dialog = Dialog(["I feel I can fly.",
                                  "I feel that I can",
                                  "touch the sky."])
        if self.time == 26:
            self.dialog = None

        if self.time == 27:
            self.add(RandomFruit(Fruit.MEDIUM, Fruit.SIDE_WEST, 320))
        if self.time == 30:
            self.add(RandomFruit(Fruit.MEDIUM, Fruit.SIDE_EAST))
            self.add(RandomFruit(Fruit.MEDIUM, Fruit.SIDE_WEST))
        if self.time == 33:
            self.add(RandomFruit(Fruit.MEDIUM, Fruit.SIDE_WEST))

        if self.time == 37:
            self.add(RandomFruit(Fruit.MEDIUM))
            self.dialog = Dialog(["This is so fun."])

        if self.time == 40:
            self.box.grow = False
            self.dialog = None

        if self.time > 37 and self.time < 60 and self.time % 2 == 0:
            self.add(RandomFruit(Fruit.LITTLE))

        if self.time == 60:
            self.dialog = Dialog(["Ok. I'm tired.",
                                  "I'm going to try",
                                  "another game."])

    def move_both(self):
        self.last_move = GameScene.M_BOTH
        self.box.set_velocity(-2 * self.box.mass)

    def move_west(self, down):
        self._check_speed(GameScene.M_WEST, down)
        self.last_move = GameScene.M_WEST
        self.box.rect.left -= self.box_speed

    def move_east(self, down):
        self._check_speed(GameScene.M_EAST, down)
        self.last_move = GameScene.M_EAST
        self.box.rect.left += self.box_speed

    def _check_speed(self, move, down):
        if self.last_move == move and down and self.down_count < 5:
            self.box_speed = 10
            self.down_count = 0
        elif down:
            self.box_speed = 2
            self.down_count = 0
        else:
            self.down_count += 1

    def update(self):
        Scene.update(self)

        self.box.update(self)
        if self.dialog:
            self.dialog.update(self.box)

    def draw(self, screen):
        Scene.draw(self, screen)

        self.box.draw(screen)
        if self.dialog:
            self.dialog.draw(screen)

