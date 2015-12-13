"""Grbox"""

import pygame
import pygame.midi

from pygame.locals import *

from .core import Manager
from .scenes import GameScene
from .data import soundfile

def main():
    pygame.init()
    pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Grbox - Grow a box!")
    pygame.time.set_timer(USEREVENT + 1, 1000)

    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()

    scenes = Manager()
    scenes.push(GameScene())

    west = False
    east = False

    while scenes.top():
        clock.tick(48)

        tick = False
        both = False

        west_down = False
        east_down = False

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == USEREVENT + 1:
                tick = True
            elif event.type == KEYDOWN and event.key == K_LEFT:
                west = True
                west_down = True
            elif event.type == KEYUP and event.key == K_LEFT:
                west = False
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                east = True
                east_down = True
            elif event.type == KEYUP and event.key == K_RIGHT:
                east = False

        if west and east:
            both = True
            west = False
            east = False

        scene = scenes.top()
        screen.fill((255, 255, 255))

        tick and scene.tick()
        west and scene.move_west(west_down)
        east and scene.move_east(east_down)
        both and scene.move_both()

        scene.update()
        scene.draw(screen)

        pygame.display.flip()
        pygame.display.update()

    pygame.quit()

