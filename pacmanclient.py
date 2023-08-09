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

    if player.lost:
        draw_text('GAME OVER', bauhaus_big, WHITE, 115, 400)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    network = Network()

    world = World(world_data)
    player_data = network.getPlayer()
    # player = Player(player_data[0], player_data[1], player_data[2])
    # local_player_group = pygame.sprite.Group()
    player_number = player_data[2]
    #local_player_group.add(player)

    while run:
        #print("1")
        # data = network.send(pickle.dumps(('Player', player.send())))
        # #print("2")
        # world.load(data)
        #print("2.25")
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        keys = pygame.key.get_pressed()
                
        pressed = -1
        if keys[pygame.K_LEFT]:
            pressed = 1
        elif keys[pygame.K_RIGHT]:
            pressed = 2
        elif keys[pygame.K_UP]:
            pressed = 3
        elif keys[pygame.K_DOWN]:
            pressed = 4
        #print("2.5")
        print(pressed)
        data = network.send(pressed)
        world.load(data)
        #print("3")

        # directions = []
        # for i in range(len(world.player_group.sprites())): #need to format it in an array so that player.update() can work
        #     if i == player.number:
        #         directions.append(pressed)
        #     else:
        #         directions.append(-1) #placeholder
        #player.update(world_data, directions)
        #print("4")

        redrawWindow(screen, world, player_number)
        #print("5")

main()
