

import pygame, pickle
from world import World, world_data
from player import Player
from network import Network

width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman Game")

pygame.init()
bauhaus = pygame.font.SysFont('Bauhaus 93', 30)
bauhaus_big = pygame.font.SysFont('Bauhaus 93', 150)
WHITE = (255,255,255)

clientNumber = 0

tile_size = 50
frame_rate = 45

STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
world = World(world_data)
while True:
    world.draw(screen)
    pygame.display.update()