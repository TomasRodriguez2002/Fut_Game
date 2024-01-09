import pygame
from Game import Game

FPS = 30

# Dimensiones de pantalla
WIDTH = 1356
HEIGHT = 755

# Paleta de colores
AZUL = (0,0,255)

# Limites de la cancha
LATERAL_IZQ = 48 # coord en y 
LATERAL_DER = 719 # coord en y
FONDO_DER = 1252 # coord en x 
FONDO_IZQ = 101 # coord en x
MITAD_CANCHA = 677 # coord en x
SAQUE = 383  # coord en y
PALO_SUP_IZQ = 317 # coord en y 
PALO_SUP_DER = 317 # coord en y
PALO_INF_IZQ = 445  # coord en y
PALO_INF_DER = 445 # coord en y
AREA_G_INF_DER = 623 # coord en y 
AREA_G_INF_IZQ = 623 # coord en y 
AREA_G_SUP_IZQ = 144 # coord en y 
AREA_G_SUP_DER = 144 # coord en y 
AREA_G_MID_DER = 1029 # coord en x 
AREA_G_MID_IZQ = 324 # coord en x
AREA_C_INF_IZQ = 527 # coord en y 
AREA_C_INF_DER = 527 # coord en y
AREA_C_SUP_IZQ =  240 # coord en y 
AREA_C_SUP_DER = 240 # coord en y 
AREA_C_MID_IZQ = 209 # coord en x 
AREA_C_MID_DER = 1144 # coord en x 

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
