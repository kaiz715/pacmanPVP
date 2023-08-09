import pygame, math


WHITE = (255,255,255)

tile_size = 50
frame_rate = 45

STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, number, direction = -1):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
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

    def load(self, player_data): # player_data = [x, y, direction, invincibility_time, score, lost]
        self.rect.x = player_data[0]
        self.rect.y = player_data[1]
        self.direction = player_data[2]
        self.invincibility_time = player_data[3]
        self.score = player_data[4]
        self.lost = player_data[5]

        if self.direction == LEFT:
            self.image = self.left
        elif self.direction == RIGHT:
            self.image = self.right
        elif self.direction == UP:
            self.image = self.up
        elif self.direction == DOWN:
            self.image = self.down

        if self.lost:
            self.image = None
    
    def send(self):
        return (self.rect.x, self.rect.y, self.direction, self.invincibility_time, self.score, self.lost)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, world_data, directions):
        if self.lost:
            return

        dx = 0
        dy = 0
        turned = False  # assume turned unless no turn
        #print(directions)
        pressed = directions[self.number]
        # if pressed == -1: #if we dont get any response from client
        #     pressed = self.direction
        
        if (self.rect.x / 50).is_integer() and (self.rect.y / 50).is_integer(): #check if position is directly in a tile
            prev_direction = self.direction
            prev_image = self.image
            if pressed == LEFT and self.direction != RIGHT:
                dx = -self.vel
                self.direction = LEFT
                self.image = self.left
                turned = True
            elif pressed == RIGHT and self.direction != LEFT:
                dx = self.vel
                self.direction = RIGHT
                self.image = self.right
                turned = True
            elif pressed == UP and self.direction != DOWN:
                dy = -self.vel
                self.direction = UP
                self.image = self.up
                turned = True
            elif pressed == DOWN and self.direction != UP:
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