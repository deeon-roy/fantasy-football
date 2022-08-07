from player import Player
from tile_map import TileMap
from team import Team
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

TICK_RATE = 144


def main():
    pygame.init()
    pygame.font.init()

    my_font = pygame.font.SysFont('Comic Sans MS', 12)
    origin = [460, -100]
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    tile_map = TileMap(origin=origin, tile_size=50, tile_amount=8)
    tile_map.create_tile_list()

    player_one = Player(100, 0, tile_map.tile_list[0].centre)
    player_two = Player(100, 4, tile_map.tile_list[4].centre)

    teams = [Team([player_one], (210, 127, 30)), Team([player_two], (30, 127, 210))]
    # team_one = Team([player_one], (210, 127, 30))
    # team_two = Team([player_two], (30, 127, 210))

    for player in teams[0].players:
        tile_map.team_map[0].append(
            [int(player.tile_index / 8), int(player.tile_index % 8)])
    for player in teams[1].players:
        tile_map.team_map[1].append(
            [int(player.tile_index / 8), int(player.tile_index % 8)])

    while True:
        mouse_pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        x, y = mouse_pos
        mouse_tile_index = tile_map.check_which_tile(x, y)

        if mouse_tile_index is not None:
            mouse_tile = tile_map.tile_list[mouse_tile_index]
            mouse_tile.toggle_hover()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_tile_index is not None:
                        tile_map.select_tile(mouse_tile_index)
                        if not mouse_tile.selected:
                            mouse_tile.toggle_hover()
                elif event.button == 3:
                    tile_map.add_collisions([[0, 1], [1, 1], [2, 2]])
                    print(tile_map.collision_map)

        _VARS['surf'].fill((115, 115, 115))
        for tile in tile_map.tile_list:
            tile.draw_tile()

        for index, tile in enumerate(tile_map.tile_list):
            # display tile indicies
            txt_surface = my_font.render(f'{index}', False, (0, 0, 0))
            _VARS['surf'].blit(txt_surface, tile.centre)
            _VARS['surf'].blit(txt_surface, (100, 0))
            pygame.draw.circle(_VARS['surf'], (0, 0, 0),
                               tile.centre, 2)

        if tile_map.path:
            # tile_map.draw_path()
            for index, node_index in enumerate(tile_map.path):
                if index - 1 > -1:
                    pygame.draw.line(_VARS['surf'], (255, 255, 255), tile_map.tile_list[tile_map.path[index-1]].centre, tile_map.tile_list[tile_map.path[index]].centre)
            
            for player in teams[tile_map.team_turn].players:
                if player.tile_index == tile_map.path[0]:                                                                           
                    player.moving = True
                    player.path = tile_map.path
                    player.path.reverse()

        for player in teams[tile_map.team_turn].players:
        
            if player.moving and player.path is not None:
                
                if player.movement_path is not None and len(player.movement_path) > 0:
                    player.move()
                elif len(player.path) > 1:
                    
                    if [int(player.path[-2] / 8), int(player.path[-2] % 8)] in tile_map.team_map[abs(tile_map.team_turn - 1)]:
                        player.path.pop()
                    else: 
                        current_tile_index = tile_map.tile_list[player.path.pop(
                        )].centre
                        destination_tile_index = tile_map.tile_list[player.path[-1]].centre
                        player.movement_path = player.generate_movement_points(
                            current_tile_index, destination_tile_index, animation_length=0.25)
                        player.tile_index = player.path[-1]
                else:
                    player.moving = False
                    player.path = None
                    player.movement_path = None
                    tile_map.path = None
                    print(player.tile_index)
                    tile_map.team_map[tile_map.team_turn] = [[int(player.tile_index / 8), int(player.tile_index % 8)]]
                    print('team map')
                    print(tile_map.team_map)
                    tile_map.team_turn = abs(tile_map.team_turn - 1)


        
        for index, team in enumerate(teams):
            team_map = []
            for player in team.players:
                team_map.append([int(player.tile_index / 8), int(player.tile_index % 8)])

            tile_map.team_map[index] = team_map 

           
        tile_map.set_collisions()
        for player in teams[0].players:
            player.draw_player()
        for player in teams[1].players:
            player.draw_player()

        pygame.display.update()
        if mouse_tile_index is not None:
            mouse_tile.toggle_hover()
        pygame.time.Clock().tick(TICK_RATE)


if __name__ == '__main__':
    main()
