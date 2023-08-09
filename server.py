import socket
from _thread import *
from world import World, world_data
from player import Player
import pickle, pygame


#start the server
server = "192.168.0.40"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

current_player = 0

#game variables
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman Game")

pygame.init()
bauhaus = pygame.font.SysFont('Bauhaus 93', 30)
bauhaus_big = pygame.font.SysFont('Bauhaus 93', 150)
WHITE = (255,255,255)

tile_size = 50
frame_rate = 45

STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

#create the game and players
players = [Player(50,50, 0), Player(50,900, 1), Player(900,50, 2), Player(900,900, 3)]
player_moves = [-1, -1, -1, -1]
world = World(world_data)
for player in players:
    world.player_group.add(player)

def threaded_client(conn, player_num):
    conn.send(pickle.dumps((players[player_num].rect.x, players[player_num].rect.y, player_num)))
    reply = None

    while True:
        try:
            data = pickle.loads(conn.recv(16384))
            
            if not data:
                print("Disconnected")
                break
            else:
                player_moves[player_num] = data
                reply = world.export()


            #print(reply)
            conn.send(pickle.dumps(reply))

        except Exception as e: 
            print(e)

def check_for_connection():
    global current_player
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, current_player))
        current_player += 1

def main():
    start_new_thread(check_for_connection, ())

    run = True
    clock = pygame.time.Clock()
    world.draw(screen)
    pygame.display.update()

    while run:
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        #update world
        if current_player == 3: #only update if all players have loaded in
            world.update(player_moves)

        #draw screen. only use for debug purposes
        screen.fill((0, 0, 0))
        world.draw(screen)
        pygame.display.update()


main()