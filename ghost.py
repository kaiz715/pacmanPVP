import pygame, random, math


WHITE = (255,255,255)

tile_size = 50

STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("images/dummyghost.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size))

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

    def load(self, ghost_data): # ghost_data = [x,y]
        self.rect.x = ghost_data[0]
        self.rect.y = ghost_data[1]

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

            #check if turn would collide with wall
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
                if self.direction == LEFT or self.direction == RIGHT: #sets up next turn direction
                    self.turn_direction = random.randint(UP,DOWN)
                elif self.direction == UP or self.direction == DOWN:
                    self.turn_direction = random.randint(LEFT,RIGHT)
                self.delay = random.randint(1,35)
            
        if self.delay > 0:
            self.delay-=1

        self.rect.x += dx #update positions
        self.rect.y += dy