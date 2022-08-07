# pygame imports
import pygame
from pygame.locals import *
# ---------------------------
from src.map.a_star import create_adjacent_list, get_shortest_distance
from src.helpers.conversions import cart_to_isometric
# other imports
import numpy as np

SCREENSIZE = WIDTH, HEIGHT = 1000, 1000

_VARS = {}

_VARS['surf'] = pygame.display.set_mode(SCREENSIZE)


class Tile:
    def __init__(self, tile_coordinates, width, height):
        self.colour = (0, 0, 0)
        self.tile_coordinates = tile_coordinates
        self.selected = False
        self.hover = False
        self.width = width
        self.height = height
        self.centre = self.get_centre_of_points(tile_coordinates)
        self.prev_colour = (0, 0, 0)

    def get_centre_of_points(self, points):
        x, y = zip(*points)
        centre = (sum(x) / len(points), sum(y) / len(points))
        return centre

    def in_tile(self, x, y):
        a = 0.5*self.width
        b = 0.5*self.height
        U = self.width/(2*a)
        V = self.height/(2*b)

        W = [x - self.centre[0], y - self.centre[1]]
        xabs = abs(W[0]*U)
        yabs = abs(W[1]*V)
        if (xabs/self.width) + (yabs/self.height) <= 1:
            return True
        else:
            return False

    def draw_tile(self):
        pygame.draw.polygon(_VARS['surf'], self.colour,
                            self.tile_coordinates, 2)

    def toggle_selected(self):
        if self.selected:
            self.selected = False
            self.colour = (0, 0, 0)
            self.prev_colour = (0, 0, 0)
        else:
            self.selected = True
            self.colour = (0, 0, 255)
            self.prev_colour = (0, 0, 255)

    def toggle_hover(self):
        if not self.selected:
            if self.colour != (255, 255, 255):
                self.hover = True
                self.prev_colour = self.colour
                self.colour = (255, 255, 255)
            else:
                self.hover = False
                self.colour = self.prev_colour


class TileMap:
    def __init__(self, origin, tile_size, tile_amount):
        self.tile_size = tile_size
        self.tile_amount = tile_amount
        self.origin = origin
        self.tile_list = []
        self.tile_coordinate_refference = []
        self.selected_tile_index = None
        self.adjacent_list, self.collision_map = create_adjacent_list(
            tile_amount)
        self.team_map = [[], []]
        self.path = None
        self.team_turn = 0

        print(self.collision_map)

    def set_collisions(self): 
        self.collision_map = np.ones(self.tile_amount**2).reshape(self.tile_amount, -1)
        for team in self.team_map:
            for collision_index in team: 
                self.collision_map[collision_index[0]][collision_index[1]] = 0
                
        self.adjacent_list, _ = create_adjacent_list(self.tile_amount, self.collision_map)

    def get_tile_coordinates(self, origin=[0, 0]):
        point_top = cart_to_isometric([origin[0], origin[1]])
        point_right = cart_to_isometric(
            [origin[0] + self.tile_size, origin[1]])
        point_bottom = cart_to_isometric(
            [origin[0] + self.tile_size, origin[1] + self.tile_size])
        point_left = cart_to_isometric(
            [origin[0], origin[1] + self.tile_size])
        coordinates = [point_top, point_right, point_bottom, point_left]

        return coordinates

    def create_tile_list(self):
        for tile_number_x in range(0, self.tile_amount):
            for tile_number_y in range(0, self.tile_amount):
                self.tile_list.append(
                    Tile(self.get_tile_coordinates(
                        [self.origin[0]+(self.tile_size*tile_number_x),
                         self.origin[1]+(self.tile_size*tile_number_y)]),
                         self.tile_size,
                         self.tile_size/2))

    def check_which_tile(self, x, y):
        for tile in self.tile_list:
            if tile.in_tile(x, y):
                return self.tile_list.index(tile)

        return None

    def draw_path(self):
        for index, node in enumerate(self.path):
            if index != len(self.path):
                pygame.draw.line(_VARS['surf'], (255, 255, 255),
                                 self.tile_list[index].centre, self.tile_list[index+1].centre)
                print(self.collision_map)

    def select_tile(self, tile_index):
        if self.selected_tile_index is not None and self.selected_tile_index != tile_index and self.tile_list[self.selected_tile_index].selected:
            if self.tile_list[self.selected_tile_index].selected:
                self.tile_list[self.selected_tile_index].toggle_selected()
            self.tile_list[tile_index].toggle_selected()
            for coordinate in self.team_map[self.team_turn]: 
                print(coordinate)
                print((coordinate[0] * 8) + coordinate[1])
                if self.selected_tile_index == (coordinate[0] * 8) + coordinate[1]: 

                    path, cost = get_shortest_distance(
                        self.adjacent_list, self.selected_tile_index, tile_index, self.tile_amount**2)
                    self.path = path
        else:
            self.path = None
            self.tile_list[tile_index].toggle_selected()
        self.selected_tile_index = tile_index

    def add_collisions(self, collision_indices):
        for index in collision_indices:
            self.collision_map[index[0]][index[1]] = 0
        self.adjacent_list, _ = create_adjacent_list(
            self.tile_amount, self.collision_map)
