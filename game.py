import sys

import pygame

import constants
from world import World


def main():
    pygame.init()
    screen = pygame.display.set_mode([constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT])
    pygame.display.set_caption("Nathan's Platformer")
    world = World()
    world.run(screen)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()