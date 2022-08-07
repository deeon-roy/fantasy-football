# pygame imports
from venv import create
import pygame
from pygame.locals import *
# ---------------------------
# other imports
import math
import sys
import time
import random

# constants
SCREENSIZE = WIDTH, HEIGHT = 1000, 1000

_VARS = {'surf': False}


def cart_to_isometric(point):
    isoX = point[0] - point[1]
    isoY = (point[0] + point[1])/2
    return [isoX, isoY]


def draw_rectangle(origin=[0, 0], width=100, height=100):
    point_top = cart_to_isometric([origin[0], origin[1]])
    point_right = cart_to_isometric([origin[0] + height, origin[1]])
    point_bottom = cart_to_isometric([origin[0] + height, origin[1] + width])
    point_left = cart_to_isometric([origin[0], origin[1] + width])
    coordinates = [point_top, point_right, point_bottom, point_left]

    pygame.draw.polygon(_VARS['surf'], (0, 0, 0), coordinates, 2)


def get_tile_coordinates(origin=[0, 0], width=100, height=100):
    point_top = cart_to_isometric([origin[0], origin[1]])
    point_right = cart_to_isometric([origin[0] + height, origin[1]])
    point_bottom = cart_to_isometric([origin[0] + height, origin[1] + width])
    point_left = cart_to_isometric([origin[0], origin[1] + width])
    coordinates = [point_top, point_right, point_bottom, point_left]

    return coordinates


def draw_isometric_grid(origin=[0, 0], size=8, cell_size=20):

    origin_list = []
    border_size = cell_size*size
    border_points = [
        cart_to_isometric(origin),
        cart_to_isometric([origin[0], border_size + origin[1]]),
        cart_to_isometric([border_size + origin[0], border_size + origin[1]]),
        cart_to_isometric([border_size + origin[0], origin[1]])
    ]

    pygame.draw.polygon(_VARS['surf'], (0, 0, 0), border_points, 2)

    lines1 = []
    lines2 = []

    for col_row in range(0, size+1):
        dimension = cell_size * col_row
        lines1.append(((cart_to_isometric([origin[0], origin[1] + dimension]),
                       cart_to_isometric([origin[0] + border_size, origin[1] + dimension]))))
        lines2.append(((cart_to_isometric([origin[0] + dimension, origin[1]]),
                        cart_to_isometric([origin[0] + dimension, origin[1] + border_size]))))
        pygame.draw.line(_VARS['surf'], (0, 0, 0),
                         cart_to_isometric([origin[0], origin[1] + dimension]),
                         cart_to_isometric([origin[0] + border_size, origin[1] + dimension]), 1)
        pygame.draw.line(_VARS['surf'], (0, 0, 0),
                         cart_to_isometric([origin[0] + dimension, origin[1]]),
                         cart_to_isometric([origin[0] + dimension, origin[1] + border_size]), 1)
        # pygame.draw.circle(_VARS['surf'], (255,255,255), cart_to_isometric([origin[0], origin[1]]), 4)
        pygame.draw.circle(_VARS['surf'], (255, 0, 255), cart_to_isometric(
            [origin[0], origin[1] + dimension]), 4)
        pygame.draw.circle(_VARS['surf'], (0, 255, 255), cart_to_isometric(
            [origin[0] + border_size, origin[1] + dimension]), 4)
        pygame.draw.circle(_VARS['surf'], (255, 255, 0), cart_to_isometric(
            [origin[0] + dimension, origin[1]]), 4)
        pygame.draw.circle(_VARS['surf'], (255, 255, 255), cart_to_isometric(
            [origin[0] + dimension, origin[1] + border_size]), 4)

        midpoints = get_midpoints_of_tiles(lines1, lines2)

        for midpoint in midpoints:
            pygame.draw.circle(_VARS['surf'], (255, 255, 255), midpoint, 4)


def get_midpoints_of_tiles(lines1, lines2):
    midpoints = []
    # midpoints.append(midpoint(lines1[1][0], lines2[1][0], lines1[1][1], lines2[1][1]))
    # midpoints.append(midpoint(lines1[-2][0], lines2[-2][0], lines1[-2][1], lines2[-2][1]))
    # print(lines2[0])
    intersection_list = [*lines2[2:], *lines1[1:]]
    for line1_index, line1 in enumerate(lines1[1:], 1):
        temp_intersection_list = []
        for line2_index, line2 in enumerate(lines2[1:], 1):
            # if line1_index == 0 or line1_index == len(lines1) -1 or line2_index:
            #     continue
            if line1_index == 1 and line2_index == 1:
                midpoints.append(
                    midpoint(line1[0][0], line2[0][0], line1[0][1], line2[0][1]))
            else:
                temp_intersection_list.append(
                    line_intersection(line1, lines2[line2_index - 1]))
                # midpoints.append(midpoint(intersection[0], line2[0][0], intersection[1], line2[0][1]))
                # midpoints
        time.sleep(0.05)
        pygame.display.update()
        intersection_list.append(temp_intersection_list)

        for line_index, line in enumerate(intersection_list):
            for item in line:
                # print(line)
                # print('---------------------')
                # print(intersection_list)
                pygame.draw.circle(_VARS['surf'], (255, 255, 255), item, 7)

    return midpoints


def midpoint(x1, x2, y1, y2):
    return ((x1+x2)/2, (y1+y2)/2)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    time.sleep(1)
    return (x, y)


def create_tile_list(origin=[660, 200], tile_amount=8, size=50):
    tile_list = []
    for tile_number_x in range(0, tile_amount):
        for tile_number_y in range(1, tile_amount+1):
            tile_list.append(get_tile_coordinates(
                origin=[origin[0]+(size*tile_number_x), origin[1]+(size*tile_number_y)]))

    return tile_list


def main():
    pygame.init()

    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        _VARS['surf'].fill((115, 115, 115))
        isometric_origin = cart_to_isometric([0, 0])
        # draw_rectangle(origin=[660,200])
        # draw_rectangle(origin=[560,100])
        # draw_rectangle(origin=[460, 0])
        # draw_rectangle(origin=[560, 0])
        # draw_rectangle(origin=[460,100])
        # draw_rectangle(origin=[460,200])
        # draw_rectangle(origin=[460,-100])

        # draw_isometric_grid(origin=[660, 200], cell_size=45)
        tile_list = create_tile_list(origin=[460, -100])
        for tile in tile_list:
            pygame.draw.polygon(_VARS['surf'], (0, 0, 0), tile, 2)
        pygame.display.update()


if __name__ == '__main__':
    main()
