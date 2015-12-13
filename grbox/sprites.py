
from pygame import Surface, Rect, draw
from pygame.font import SysFont
from pygame.image import load as load_image
from pygame.sprite import Sprite, spritecollide

from random import randint
from .data import imagefruit

class HorizonLine(Sprite):
    def __init__(self, color, height=4):
        Sprite.__init__(self)

        self.image = Surface((640, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.top = 384

class Box(Sprite):
    def __init__(self, color, mass):
        Sprite.__init__(self)

        self.grow = True

        self.color = color
        self.size = mass * 10
        self.mass = mass

        self.image = Surface((self.size, self.size))
        self.image.fill(color)

        draw.rect(self.image, (0,0,0), (0, 0, self.size, self.size), 1)

        self.rect = self.image.get_rect()
        self.rect.center = (320, 344)

        self.acceleration = 2
        self.velocity = 0

        self.time = 0
        self.vpos = self.rect.top

    def set_velocity(self, velocity):
        self.acceleration = 2 if velocity else 0
        self.velocity = velocity
        self.time = 0
        self.vpos = self.rect.top

    def uplevel(self):
        if not self.grow:
            return

        self.mass += 1
        self.size = self.mass * 10

        self.image = Surface((self.size, self.size))
        self.image.fill(self.color)

        draw.rect(self.image, (0,0,0), (0, 0, self.size, self.size), 1)

    def update(self, group=None):
        collide = spritecollide(self, group, False)

        self.rect.width = self.size
        self.rect.height = self.size

        hit_floor = False

        if group and collide:
            for sprite in collide:
                if type(sprite) is HorizonLine:
                    hit_floor = True
                else:
                    group.remove(sprite)
                    self.uplevel()

        if self.acceleration:
            self.rect.top = self.vpos \
                          + (self.velocity * self.time) \
                          + (self.acceleration / 2) * (self.time ** 2)
            self.time += 1

        if hit_floor or not self.acceleration:
            self.rect.bottom = 384
            self.set_velocity(0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Dialog(Sprite):
    def __init__(self, texts):
        Sprite.__init__(self)

        width = 0
        height = 0
        space = 6
        between = 3

        font = SysFont("monospace", 18)
        for text in texts:
            f_width, f_height = font.size(text)

            height += f_height + between
            if f_width > width:
                width = f_width

        self.image = Surface((width + space * 2, height + space * 2))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()

        draw.rect(self.image, (0,0,0), self.rect, 1)

        top = space
        for text in texts:
            self.image.blit(font.render(text, 1, (0, 0, 0)), (space, top))
            top += font.get_linesize() + between

    def update(self, follow):
        self.rect.left = follow.rect.right + 6
        self.rect.bottom = follow.rect.top - 6

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fruit(Sprite):
    VERTICAL = 1
    SIDE_WEST = 2
    SIDE_EAST = 3

    LITTLE = "little"
    MEDIUM = "medium"
    NORMAL = "normal"

    def __init__(self, name, size, direction, position, speed=None):
        Sprite.__init__(self)

        self.image = load_image(imagefruit(name, size))
        self.image.set_colorkey((255, 0, 255))
        self.rect = self.image.get_rect()

        self.direction = direction

        if direction == Fruit.VERTICAL:
            self.rect.centerx = position
        else:
            self.rect.centery = position
            if direction == Fruit.SIDE_WEST:
                self.rect.left = 640

        if not speed:
            speed = 1
            if name == Fruit.MEDIUM:
                speed += 1
            if name == Fruit.LITTLE:
                speed += 4

        self.speed = speed

    def update(self):
        if self.direction == Fruit.VERTICAL:
            self.rect.top += self.speed
        elif self.direction == Fruit.SIDE_WEST:
            self.rect.left -= self.speed
        elif self.direction == Fruit.SIDE_EAST:
            self.rect.left += self.speed

class RandomFruit(Fruit):
    names = ['apple', 'cherry', 'strawberry']

    def __init__(self, size, direction=None, position=None):
        name = RandomFruit.names[randint(0, 2)]

        if not direction:
            direction = randint(1, 3)

        if not position:
            if direction == Fruit.VERTICAL:
                position = randint(8, 632)
            else:
                position = randint(8, 376)

        Fruit.__init__(self, name, size, direction, position)

