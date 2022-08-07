import pygame
from pygame.locals import *
import numpy as np

SCREENSIZE = WIDTH, HEIGHT = 1000, 1000

_VARS = {}

_VARS['surf'] = pygame.display.set_mode(SCREENSIZE)

class Team(): 
    def __init__(self, players, colour):
        self.players = players
        self.colour = colour
        self.turn = False
        self.state = None

        for player in self.players: 
            player.colour = colour
