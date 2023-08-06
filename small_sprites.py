import pygame

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