import pygame

from spritesheet_functions import get_path_name


def get_anamations(spritesheet, hitbox, textfile, scale):
    spritesheet = get_path_name("images", spritesheet)
    spritesheet = pygame.image.load(spritesheet).convert_alpha()
    hitbox = get_path_name("images",hitbox)
    hitbox = pygame.image.load(hitbox).convert_alpha()
    anamations = {}
    anamations_hitbox = {}
    with open(get_path_name("animations", textfile)) as f:
        lines = f.readlines()
        i=0
        starting_y = 0
        while i < len(lines):
            # hardcoded idle anamation
            anamationName = lines[i].strip()
            dimensions = lines[i+1].strip().split("x")
            dimensions = [int(x) for x in dimensions]
            dashes = lines[i+2]
            starting_x = 0
            anamations[anamationName] = get_anamation_row(dimensions, spritesheet, scale, starting_x, starting_y)
            anamations_hitbox[anamationName] = get_anamation_row(dimensions,hitbox,scale,starting_x,starting_y)
            starting_y += dimensions[1] #add the height of the previous row
            i+=3
    return anamations, anamations_hitbox


def clock():
    curent_time = pygame.time.get_ticks()
    return curent_time


def get_anamation_row(dimensions: list, spritesheet, scale, sx, sy):
    width = dimensions[0]
    height = dimensions[1]
    colums = dimensions[2]
    anamationSpeed = dimensions[3]
    row = []
    for c in range(colums):
        image = pygame.Surface([dimensions[0], dimensions[1]], pygame.SRCALPHA)
        image.blit(spritesheet, (0, 0), (sx, sy, dimensions[0], dimensions[1]))
        sx += width
        if scale != 1:
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        row.append(image)
    return row

def get_hitbox_image(image):
    pxarray = pygame.PixelArray(image)
    black_white_array = pxarray.extract(0xFFFFFF)
    print(black_white_array)
    return black_white_array.make_surface()


class Anamation:
    def __init__(self, spritesheet, hitbox, textfile, scale):
        self.anamations,self.anamations_hitbox = get_anamations(spritesheet,hitbox, textfile, scale)
        self.anamation_speed = 80  # ms
        self.curent_frame = 0
        self.time_of_next_frame = clock() + self.anamation_speed
        self.anamation_name = "Attack-1"

    def update_anamation(self,name):
        if self.anamation_name != name:
            self.anamation_name = name
            self.time_of_next_frame = clock() + self.anamation_speed
            self.curent_frame = 0

    def update(self):
        if clock() > self.time_of_next_frame:
            self.curent_frame = (self.curent_frame + 1) % len(self.anamations[self.anamation_name])
            self.time_of_next_frame += self.anamation_speed

    def get_image(self):
        return self.anamations[self.anamation_name][self.curent_frame], self.anamations_hitbox[self.anamation_name][self.curent_frame]
