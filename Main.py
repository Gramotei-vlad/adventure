from Game.GameLoop import Game

import pygame


if __name__ == '__main__':
    pygame.init()
    GameClass = Game()
    GameClass.start_game()
