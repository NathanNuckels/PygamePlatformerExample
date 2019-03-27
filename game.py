import sys

import pygame

import constants
from player import Player
from room import Room

pygame.init()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
rooms = [Room("level1.txt"), Room("level2.txt")]
current_room = 0


def shit_room(direction, player):
    global current_room
    if direction == "left":
        current_room -= 1
        player.rect.x = constants.SCREEN_WIDTH - player.rect.width - 5
    elif direction == "right":
        current_room += 1
        player.rect.x = player.rect.width + 5
    if current_room < 0:
        current_room = len(rooms) - 1
    elif current_room >= len(rooms):
        current_room = 0


def main():
    pygame.display.set_caption("Walls and Rooms")
    sprites = pygame.sprite.Group()

    player = Player(0, 0, 50, 50)
    clock = pygame.time.Clock()

    sprites.add(player)
    done = False
    while not done:
        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                player.key_down(event.key)
            elif event.type == pygame.KEYUP:
                player.key_up(event.key)

        # --- Game Logic ---
        player.set_room(rooms[current_room])
        sprites.update()
        rooms[current_room].update()
        # Player status
        if player.rect.x <= -player.rect.width:
            shit_room("left", player)
        elif player.rect.x >= constants.SCREEN_WIDTH:
            shit_room("right", player)

        # --- Drawing ---
        rooms[current_room].draw(screen)
        sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
