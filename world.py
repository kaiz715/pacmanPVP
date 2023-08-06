import pygame
from small_sprites import Wall, Coin, Fruit
from ghost import Ghost
from player import Player

width = 1000
height = 1000

WHITE = (255,255,255)

clientNumber = 0

tile_size = 50
frame_rate = 45

STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 2, 2, 1, 3, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 0, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1],
    [1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 3, 2, 2, 2, 2, 3, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1],
    [1, 3, 1, 2, 2, 2, 1, 2, 1, 4, 4, 1, 2, 1, 2, 2, 2, 1, 3, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 4, 4, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1],
    [1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1],
    [1, 0, 2, 2, 2, 2, 1, 3, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class World:
    def __init__(self, data):
        self.world_data = data
        self.coin_group = pygame.sprite.Group()
        self.fruit_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        # populating groups based on world data
        for y in range(len(data)):  # each row
            for x in range(len(data[y])):  # each col
                if data[y][x] == 1:
                    wall = Wall(x * tile_size, y * tile_size)
                    self.wall_group.add(wall)
                elif data[y][x] == 2:
                    coin = Coin(
                        x * tile_size + (tile_size // 2),
                        y * tile_size + (tile_size // 2),
                    )
                    self.coin_group.add(coin)  # center the coin on the tile
                elif data[y][x] == 3:
                    fruit = Fruit(
                        x * tile_size + (tile_size // 2),
                        y * tile_size + (tile_size // 2),
                    )
                    self.fruit_group.add(fruit)  # center the fruit on the tile
                elif data[y][x] == 4:
                    ghost = Ghost(x * tile_size, y * tile_size)
                    self.ghost_group.add(ghost)


    def draw(self, screen):
        self.wall_group.draw(screen)
        self.coin_group.draw(screen)
        self.fruit_group.draw(screen)

        #update and draw ghost
        self.ghost_group.update(self.world_data)
        self.ghost_group.draw(screen)

        #update and draw player
        self.player_group.update(self.world_data)
        self.player_group.draw(screen)
