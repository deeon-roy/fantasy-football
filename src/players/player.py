import pygame
from pygame.locals import *
import numpy as np

SCREENSIZE = WIDTH, HEIGHT = 1000, 1000

_VARS = {}

_VARS['surf'] = pygame.display.set_mode(SCREENSIZE)


class Player:
    def __init__(self, health, tile_index, location_coordinates):
        self.colour = (127, 30, 80)
        self.health = health
        self.tile_index = tile_index
        self.location_coordinates = location_coordinates
        self.moving = False
        self.path = None
        self.movement_path = None 

    def draw_player(self):
        pygame.draw.circle(_VARS['surf'], self.colour,
                           self.location_coordinates, 4)

    def move(self): 
        self.location_coordinates = self.movement_path.pop()

    def generate_movement_points(self, p1, p2, no_of_points=144, animation_length=1):
        no_of_points = int(no_of_points * animation_length)
        movement_path = list(zip(np.linspace(p1[0], p2[0], no_of_points+1), np.linspace(p1[1], p2[1], no_of_points+1)))
        movement_path.reverse()
        return movement_path