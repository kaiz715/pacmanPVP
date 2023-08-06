import pygame
from world import World, world_data
from player import Player

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