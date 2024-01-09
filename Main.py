import pygame
from Game import Game
from Constantes import *

def main():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])#, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False
    background = pygame.image.load("estadio2.png").convert() 
    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen, background)
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
