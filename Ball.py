import pygame
from Constantes import *

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("ball1.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 785, self.image.get_height() - 785))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2) 
        #self.move_speed = 30
        #self.is_moving = False
        #self.target_rect = self.rect.copy()
        #self.teammates = []

    def update(self):

        self.rect.x += 10
        self.rect.y -= 5
        
        # Limites cancha
        
        # gol arco derecho -> saque del centro
        if self.rect.left > FONDO_DER and self.rect.top < PALO_SUP and self.rect.bottom > PALO_INF:
            # self.referee.
            # self.rect.center = (MITAD_CANCHA, SAQUE)

        # gol arco izquierdo -> saque del centro
        if self.rect.right < FONDO_IZQ and self.rect.top < PALO_SUP and self.rect.bottom > PALO_INF:
            # self.rect.center = (MITAD_CANCHA, SAQUE)

        # Si la posición en y de la pelota supera algun lateral -> efecto rebote en y
        if self.rect.top >= LATERAL_IZQ or self.rect.bottom <= LATERAL_DER:
            self.rect.y *= -1

        # Si la posición en y de la pelota no se encuentra entre los palos y la posicion en x supera la linea de fondo (der o izq) -> efecto rebote en x 
        if (self.rect.top >= PALO_SUP or self.rect.bottom <= PALO_INF) and (self.rect.left <= FONDO_IZQ or self.rect.right >= FONDO_DER):
            self.rect.x *= -1


