import pygame

from spritesheet_functions import get_path_name


def get_anamations(spritesheet, textfile, scale):
    spritesheet = get_path_name("images", spritesheet)
    spritesheet = pygame.image.load(spritesheet).convert_alpha()
    anamations = {}
    with open(get_path_name("animations", textfile)) as f:
        lines = f.readlines()
        # hardcoded idle anamation
        anamationName = lines[6].strip()
        dimensions = lines[7].strip().split("x")
        dimensions = [int(x) for x in dimensions]
        starting_x = 0
        starting_y = 107
        anamations[anamationName] = get_anamation_row(dimensions, spritesheet, scale, starting_x, starting_y)
    return anamations


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
    print("PIXEL ARRAY",pxarray)


class Anamation:
    def __init__(self, spritesheet, textfile, scale):
        self.anamations = get_anamations(spritesheet, textfile, scale)
        self.anamation_speed = 80  # ms
        self.curent_frame = 0
        self.time_of_next_frame = clock() + self.anamation_speed
        self.anamation_name = "Walking"
        get_hitbox_image(self.anamations[self.anamation_name][0])

    def update_anamation(self,name):
        if self.anamation_name != name:
            self.anamation_name = name
            self.time_of_next_frame = clock() + self.anamation_speed
            self.curent_frame = 0

    def update(self):
        if clock() > self.time_of_next_frame:
            self.curent_frame = (self.curent_frame + 1) % len(self.anamations[self.anamation_name])
            self.time_of_next_frame += self.anamation_speed

    def get_image(self, anamations_name):
        return self.anamations[anamations_name][self.curent_frame]
