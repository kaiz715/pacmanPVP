import pygame
import math, random

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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/pacmanyellow.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size))

        self.right = self.image
        self.left = pygame.transform.rotate(self.image, 180)
        self.up = pygame.transform.rotate(self.image, 90)
        self.down = pygame.transform.rotate(self.image, 270)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel = 5

        self.direction = STOPPED
        self.invincibility_time = 0
        self.score = 0
        self.lost = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, world_data):
        dx = 0
        dy = 0
        turned = False  # assume turned unless no turn
        keys = pygame.key.get_pressed()

        if (self.rect.x / 50).is_integer() and (self.rect.y / 50).is_integer(): #check if position is directly in a tile
            prev_direction = self.direction
            prev_image = self.image
            if keys[pygame.K_LEFT] and self.direction != RIGHT:
                dx = -self.vel
                self.direction = LEFT
                self.image = self.left
                turned = True
            elif keys[pygame.K_RIGHT] and self.direction != LEFT:
                dx = self.vel
                self.direction = RIGHT
                self.image = self.right
                turned = True
            elif keys[pygame.K_UP] and self.direction != DOWN:
                dy = -self.vel
                self.direction = UP
                self.image = self.up
                turned = True
            elif keys[pygame.K_DOWN] and self.direction != UP:
                dy = self.vel
                self.direction = DOWN
                self.image = self.down
                turned = True

            #check if turn would collide
            if (
                world_data[self.rect.y // 50][math.ceil((self.rect.x + dx) / 50)] == 1
                or world_data[self.rect.y // 50][math.floor((self.rect.x + dx) / 50)] == 1
                or world_data[math.ceil((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
                or world_data[math.floor((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
            ):
                dx = 0
                dy = 0
                turned = False
                self.direction = prev_direction
                self.image = prev_image

        if not turned:  # no valid key is pressed
            if self.direction == LEFT:
                dx = -self.vel
            elif self.direction == RIGHT:
                dx = self.vel
            elif self.direction == UP:
                dy = -self.vel
            elif self.direction == DOWN:
                dy = self.vel

            # check if movement will hit a wall
            if (
                    world_data[self.rect.y // 50][math.ceil((self.rect.x + dx) / 50)] == 1
                    or world_data[self.rect.y // 50][math.floor((self.rect.x + dx) / 50)] == 1
                    or world_data[math.ceil((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
                    or world_data[math.floor((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
            ):
                dx = 0
                dy = 0

        self.rect.x += dx
        self.rect.y += dy

        #adjust invincibility timer
        if self.invincibility_time > 0:
            self.invincibility_time -= 1/frame_rate


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/dummyghost.png")
        self.image = pygame.transform.scale(img, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel = 5

        self.direction = random.randint(1,4)
        if self.direction == 1 or self.direction == 2:
            self.turn_direction = random.randint(3,4)
        elif self.direction == 3 or self.direction == 4:
            self.turn_direction = random.randint(1,2)
        self.delay = 35

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, world_data):
        dx = 0
        dy = 0
        turned = False  # assume turned unless no turn

        if self.delay == 0 and (self.rect.x / 50).is_integer() and (self.rect.y / 50).is_integer(): #check if position is directly in a tile
            prev_direction = self.direction
            temp_dir = self.turn_direction
            if self.turn_direction == LEFT and self.direction != RIGHT:
                dx = -self.vel
                self.direction = LEFT
                turned = True
                self.turn_direction = random.randint(UP,DOWN)
            elif self.turn_direction == RIGHT and self.direction != LEFT:
                dx = self.vel
                self.direction = RIGHT
                turned = True
                self.turn_direction = random.randint(UP,DOWN)
            elif self.turn_direction == UP and self.direction != DOWN:
                dy = -self.vel
                self.direction = UP
                turned = True
                self.turn_direction = random.randint(LEFT,RIGHT)
            elif self.turn_direction == DOWN and self.direction != UP:
                dy = self.vel
                self.direction = DOWN
                turned = True
                self.turn_direction = random.randint(LEFT,RIGHT)
            if turned:
                self.delay = random.randint(1,35)

            #check if turn would collide
            if (
                world_data[self.rect.y // 50][math.ceil((self.rect.x + dx) / 50)] == 1
                or world_data[self.rect.y // 50][math.floor((self.rect.x + dx) / 50)] == 1
                or world_data[math.ceil((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
                or world_data[math.floor((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
            ):
                dx = 0
                dy = 0
                turned = False
                self.direction = prev_direction
                self.turn_direction = temp_dir

        if not turned:  # no valid turn is pressed
            if self.direction == LEFT:
                dx = -self.vel
            elif self.direction == RIGHT:
                dx = self.vel
            elif self.direction == UP:
                dy = -self.vel
            elif self.direction == DOWN:
                dy = self.vel

            # check if movement will hit a wall
            temp_dir = 0 #store temporary direction for checking
            while (
                    world_data[self.rect.y // 50][math.ceil((self.rect.x + dx) / 50)] == 1
                    or world_data[self.rect.y // 50][math.floor((self.rect.x + dx) / 50)] == 1
                    or world_data[math.ceil((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
                    or world_data[math.floor((self.rect.y + dy) / 50)][self.rect.x // 50] == 1
            ):
                turned = True
                if self.direction == LEFT or self.direction == RIGHT:
                    dy = random.choice((-5, 5))
                    dx = 0
                    temp_dir = (DOWN if dy == 5 else UP)

                else:
                    dx = random.choice((-5, 5))
                    dy = 0
                    temp_dir = (RIGHT if dx == 5 else LEFT)

            if turned:
                self.direction = temp_dir
                if self.direction == LEFT or self.direction == RIGHT:
                    self.turn_direction = random.randint(UP,DOWN)
                elif self.direction == UP or self.direction == DOWN:
                    self.turn_direction = random.randint(LEFT,RIGHT)
                self.delay = random.randint(1,35)
            
                
        if self.delay > 0:
            self.delay-=1
        self.rect.x += dx
        self.rect.y += dy


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):  # x and y are center
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/point.png")
        self.image = pygame.transform.scale(img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):  # x and y are center
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/strawberry.png")
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/blue.png")
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class World:
    def __init__(self, data):
        self.world_data = data
        self.coin_group = pygame.sprite.Group()
        self.fruit_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        
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

        # self.player_group.add(self.player)

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

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def redrawWindow(screen, world, player, local_player_group):
    screen.fill((0, 0, 0))

    local_player_group.draw(screen)
    #draw sprites
    world.draw(screen)

    #draw HUD
    draw_text('Score: ' + str(player.score), bauhaus, WHITE, tile_size, 10)

    if player.invincibility_time>0:
        draw_text("INVINCIBILITY ON", bauhaus, WHITE, 715, 10)

    if player.lost:
        draw_text('GAME OVER', bauhaus_big, WHITE, 115, 400)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    world = World(world_data)
    player = Player(50,50)
    local_player_group = pygame.sprite.Group()
    local_player_group.add(player)

    while run:
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.update(world_data)

        #check collisons
        if pygame.sprite.spritecollide(player, world.coin_group, True):
            player.score += 10
    
        if pygame.sprite.spritecollide(player, world.fruit_group, True):
            player.invincibility_time += 8

        if pygame.sprite.spritecollide(player, world.ghost_group, False):
            if player.invincibility_time > 0:
                pygame.sprite.spritecollide(player, world.ghost_group, True)
            else:
                player.kill()
                player.lost = True

        redrawWindow(screen, world, player, local_player_group)

main()