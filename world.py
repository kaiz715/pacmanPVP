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
    def __init__(self, world_data):
        self.world_data = world_data
        self.coin_group = pygame.sprite.Group()
        self.fruit_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        # populating groups based on world data
        for y in range(len(world_data)):  # each row
            for x in range(len(world_data[y])):  # each col
                if world_data[y][x] == 1:
                    wall = Wall(x * tile_size, y * tile_size)
                    self.wall_group.add(wall)
                elif world_data[y][x] == 2:
                    coin = Coin(
                        x * tile_size + (tile_size // 2),
                        y * tile_size + (tile_size // 2),
                    )
                    self.coin_group.add(coin)  # center the coin on the tile
                elif world_data[y][x] == 3:
                    fruit = Fruit(
                        x * tile_size + (tile_size // 2),
                        y * tile_size + (tile_size // 2),
                    )
                    self.fruit_group.add(fruit)  # center the fruit on the tile
                elif world_data[y][x] == 4:
                    ghost = Ghost(x * tile_size, y * tile_size)
                    self.ghost_group.add(ghost)

    def export(self):
        data = [[],[],[],[]] #[coin[], fruit[], ghost[], player[]]
        for coin in self.coin_group.sprites():
            data[0].append((coin.x, coin.y))
        for fruit in self.fruit_group.sprites():
            data[1].append((fruit.x, fruit.y))
        for ghost in self.ghost_group.sprites():
            data[2].append((ghost.rect.x, ghost.rect.y))
        for player in self.player_group.sprites():
            data[3].append(player.send())

        return data
            
        

    def load(self, data):
        coins = self.coin_group.sprites()
        for i in range(max(len(coins), len(data[0]))):
            if i >= len(data[0]):
                coins[i].kill()
            else:
                coins[i].load(data[0][i])

        fruits = self.fruit_group.sprites()
        for i in range(max(len(fruits), len(data[1]))):
            if i >= len(data[1]):
                fruits[i].kill()
            else:
                fruits[i].load(data[1][i])

        ghosts = self.ghost_group.sprites()
        for i in range(max(len(ghosts), len(data[2]))):
            if i >= len(data[2]):
                ghosts[i].kill()
            else:
                ghosts[i].load(data[2][i])

        players = self.player_group.sprites()
        for i in range(max(len(players), len(data[3]))):
            if i >= len(players):
                self.player_group.add(Player(data[3][i][0],data[3][i][1], i))
            else:
                players[i].load(data[3][i])
        
        
    def update(self, directions):
        #check for collisions and interactions
        for player in self.player_group.sprites():
            if pygame.sprite.spritecollide(player, self.coin_group, True):
                player.score += 10

            if pygame.sprite.spritecollide(player, self.fruit_group, True):
                player.invincibility_time += 8

            if pygame.sprite.spritecollide(player, self.ghost_group, False):
                if player.invincibility_time > 0:
                    pygame.sprite.spritecollide(player, self.ghost_group, True)
                    player.score += 100
                else:
                    player.lost = True

        #calculate and update locations
        self.ghost_group.update(self.world_data)
        self.player_group.update(self.world_data, directions)


    def draw(self, screen, player_num = -1):
        #draw each sprite group
        self.wall_group.draw(screen)
        self.coin_group.draw(screen)
        self.fruit_group.draw(screen)
        self.ghost_group.draw(screen)

        group = pygame.sprite.Group() #dont display dead players
        for player in self.player_group.sprites():
            if player.number != player_num and not player.lost:
                group.add(player)
        group.draw(screen)

        
