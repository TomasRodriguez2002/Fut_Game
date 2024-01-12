from players.Player import Player
from Constantes import * 
import pygame

class GoalKeeper(Player):

    def __init__(self, spritePNG, strategy, mediator, team):
        super().__init__(strategy, mediator, team)

        self.image = pygame.image.load(spritePNG).convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 485, self.image.get_height() - 485))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        # True -> team1 | False -> team2 
        if super.team:
            self.rect.center = (FONDO_IZQ+7, SAQUE)
        else:
            self.rect.center = (FONDO_DER-7, SAQUE)

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

            # Verificar límites laterales
            if AREA_G_SUP-7 < new_y < AREA_G_INF - self.rect.height+7:
                # Verificar límites de fondo
                flag = False
                if self.team:
                    if FONDO_IZQ-5 < new_x < AREA_G_MID_IZQ - self.rect.width+5:
                        flag = True
                else:
                    if AREA_G_MID_DER-5 < new_x < FONDO_DER - self.rect.width+5:
                        flag = True
                if flag:
                    super.animation_of_move()