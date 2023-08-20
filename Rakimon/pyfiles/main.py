# Main file

import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

pygame.quit()

# to do : true to find out a ways to suppress item on the map when collected
