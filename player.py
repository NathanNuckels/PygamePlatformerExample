import pygame

import constants
from spritesheet_functions import SpriteSheet


class Player(pygame.sprite.Sprite):
    right = False
    left = False
    up = False
    down = False
    scale = 1.75
    space=False

    def __init__(self, x, y):
        super().__init__()
        spritesheet = SpriteSheet("tiles_spritesheet.png")
        self.image = spritesheet.get_image(0,0,70,70,0.75)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        # Set speed vector of player
        self.delta_x = 5
        self.delta_y = 5
        self.room = None

    def set_room(self, room):
        self.room = room

    def process_keys(self,keys):
        self.down = keys[pygame.K_DOWN]
        self.up = keys[pygame.K_UP]
        self.left = keys[pygame.K_LEFT]
        self.right = keys[pygame.K_RIGHT]
        self.space = keys[pygame.K_SPACE]
        if self.up:
            self.jump()
    def draw(self,surface):
        self.rect = self.rect.clamp(surface.get_rect())
        surface.blit(self.image,self.rect)

    def calc_gravity(self):
        '''Calculate gravity'''
        if self.delta_y == 0:
            self.delta_y = 1
        else:
            self.delta_y += 0.35
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.delta_y >= 0:
            self.delta_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ called whan user hits up"""
        # move down and find if there is a platform below
        # one pixel isnt enough so use 2
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        self.rect.y -= 2
        # if it is ok to jump set speed t go up
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.delta_y = -10

    # Use booleans for movement and update based on booleans in update method
    def update(self):
        #set gravity
        self.calc_gravity()
        """ Move the player. """

        # Move left/right
        if self.right:
            self.rect.x += self.delta_x
        elif self.left:
            self.rect.x -= self.delta_x

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.right:
                self.rect.right = block.rect.left
            elif self.left:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.delta_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.room.collision_blocks, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.delta_y < 0:
                self.rect.top = block.rect.bottom
            elif self.delta_y > 0:
                self.rect.bottom = block.rect.top
            self.delta_y = 0
