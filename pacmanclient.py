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
bauhaus_medium = pygame.font.SysFont('Bauhaus 93', 120)
WHITE = (255,255,255)

clientNumber = 0

tile_size = 50
frame_rate = 45

STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4



def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def redrawWindow(screen, world, player_num):
    screen.fill((0, 0, 0))

    #draw sprites
    world.draw(screen)

    player = world.player_group.sprites()[player_num]
    #draw HUD
    draw_text('Player ' + str(player_num+1) + "   Score: " + str(player.score), bauhaus, WHITE, tile_size, 10)

    if player.invincibility_time>0:
        draw_text("INVINCIBILITY ON", bauhaus, WHITE, 715, 10)

    if world.winner:
        draw_text('WINNER: PLAYER ' + str(world.winner+1), bauhaus_medium, WHITE, 50, 400)
    elif player.dead:
        draw_text('YOU DIED', bauhaus_big, WHITE, 150, 400)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    network = Network()

    world = World(world_data)
    player_data = network.getPlayer()
    player_number = player_data[2]

    while run:
        clock.tick(frame_rate) #update clock
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed() #get input
        pressed = -1
        if keys[pygame.K_LEFT]:
            pressed = 1
        elif keys[pygame.K_RIGHT]:
            pressed = 2
        elif keys[pygame.K_UP]:
            pressed = 3
        elif keys[pygame.K_DOWN]:
            pressed = 4

        data = network.send(pressed) #get updated world from server
        world.load(data)

        redrawWindow(screen, world, player_number)


main()