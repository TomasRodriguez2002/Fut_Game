from IPlayer import IPlayer
from Constantes import * 
import pygame

class PlayerField(IPlayer):
    def __init__(self, coor_x, coor_y, spritePNG, strategy, mediator, team):
        super().__init__(strategy, mediator, team)
        self.image = pygame.image.load(spritePNG).convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 485, self.image.get_height() - 485))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        self.rect.center = (coor_x, coor_y)

    def update(self):
        
        #si la distancia entre el jugador y la pelota es menor que 20 entonces el jugador tiene la pelota
        super.mediator.check_collision_with_ball(self)
        
        if self.hasBall:
            
            action = super.strategy.with_ball(self, super.mediator)

            # patear
            if action == 1:
                super.mediator.shot_ball(super.team)
                super.hasBall = False
            # pasar pelota
            elif action == 2:
                x, y = super.strategy.where_to_pass(self, super.mediator)
                super.mediator.pass_ball(x, y)
                super.hasBall = False
            # moverse
            elif action == 3:
                target_x, target_y = super.strategy.getProxPos(self, super.mediator)

        else:

            target_x, target_y = super.strategy.getProxPos()

            new_x, new_y = super.calculate_new_pos(target_x, target_y)

            # Verificar límites laterales y de fondo
            if LATERAL_IZQ - 7 < new_y < LATERAL_DER - self.rect.height + 7 and \
                FONDO_IZQ - 5 < new_x < FONDO_DER - self.rect.width + 5:
                # Verificar la distancia con los compañeros
                if super.mediator.can_move(super.team, new_x, new_y):
                    super.animation_of_move()