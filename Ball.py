import pygame
from Constantes import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, mediator, spritePNG):
        super().__init__()

        self.image = pygame.image.load(spritePNG).convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 785, self.image.get_height() - 785))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = (MITAD_CANCHA, SAQUE) 
        self.move_speed = 0#35
        self.is_moving = False
        self.dx = 0
        self.dy = 0
        self.distance = 0
        self.game = game
        self.mediator = mediator

    def detect_goal(self):
        if self.rect.left > FONDO_DER and self.rect.centery < PALO_INF and self.rect.centery > PALO_SUP:
            self.is_moving = False
            self.mediator.restart_positions(True)
            return True        
        if self.rect.right < FONDO_IZQ and self.rect.centery < PALO_INF and self.rect.centery > PALO_SUP:    
            self.is_moving = False
            self.mediator.restart_positions(False)
            return True
        return False

    def detect_limits(self):
        if self.detect_goal():
            self.game.show_goal_message("¡Goooaaal!", 25)  # Ajusta la duración según sea necesario
        
        if (self.rect.top <= LATERAL_IZQ) or (self.rect.bottom >= LATERAL_DER):
            # Si la pelota se frenó fuera de la cancha -> saque del arco izq
            if self.move_speed <= 0:
                if self.rect.centerx <= MITAD_CANCHA:
                    self.mediator.restart_positions2(True)
                else:
                    self.mediator.restart_positions2(False)
            # efecto rebote en y
            else: 
                self.dy *= -1
            
        # Si la posición en y de la pelota no se encuentra entre los palos y la posicion en x supera la linea de fondo (der o izq) -> efecto rebote en x 
        if (self.rect.left <= FONDO_IZQ) or (self.rect.right >= FONDO_DER):
            if (self.rect.bottom >= PALO_INF or self.rect.top <= PALO_SUP):
                # Si la pelota se frenó fuera de la cancha -> saque del arco izq
                if self.move_speed <= 0:
                    if self.rect.centerx <= MITAD_CANCHA:
                        self.mediator.restart_positions2(True)
                    else:
                        self.mediator.restart_positions2(False)
                # efecto rebote en x
                else:
                    self.dx *= -1

    def animation_of_move(self):
        if self.move_speed != 0 and self.distance != 0:
            self.rect.x += self.dx / self.distance * self.move_speed
            self.rect.y += self.dy / self.distance * self.move_speed
            self.move_speed -= 1
        # AL REFEREE    
        if self.move_speed <= 0 or self.mediator.check_collision_with_players():    
            self.move_speed = 35
            self.is_moving = False

    def set_prox_pos(self, x, y):
        self.dx = x - self.rect.centerx
        self.dy = y - self.rect.centery
        self.distance = (self.dx ** 2 + self.dy ** 2) ** 0.5
        self.is_moving = True

    def update(self):

        self.detect_limits()

        if self.is_moving:
            self.animation_of_move()