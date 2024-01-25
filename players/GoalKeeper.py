from players.Player import Player
from Constantes import *

class GoalKeeper(Player):

    def __init__(self, spritePNG, strategy, mediator, team):
        super().__init__(spritePNG, strategy, mediator, team)
        # True -> team1 | False -> team2 
        if self.team:
            self.rect.center = (FONDO_IZQ+10, SAQUE)
        else:
            self.rect.center = (FONDO_DER-10, SAQUE)

    def move(self):
        target_x, target_y = self.strategy.getProxPos(self)
        new_x, new_y = self.calculate_new_pos(target_x, target_y)

        # Verificar límites laterales
        if AREA_G_SUP-7 < new_y < AREA_G_INF - self.rect.height+7:
            # Verificar límites de fondo
            flag = False
            if self.team:
                if FONDO_IZQ - 5 < new_x < AREA_G_MID_IZQ - self.rect.width + 5:
                    flag = True
            else:
                if AREA_G_MID_DER - 5 < new_x < FONDO_DER - self.rect.width + 5:
                    flag = True
            if flag:
                self.animation_of_move()

    def update(self):
        
        #si la distancia entre el jugador y la pelota es menor que 20 entonces el jugador tiene la pelota
        self.mediator.check_collision_with_ball(self)
        
        if self.hasBall:
            
            action = self.strategy.with_ball(self)

            # patear
            if action == SHOT:
                self.mediator.shot_ball(self.team)
                self.hasBall = False
            # pasar pelota
            elif action == PASS:
                x, y = self.strategy.where_to_pass(self)
                self.mediator.pass_ball(x, y)
                self.hasBall = False
            # moverse
            elif action == MOVE:
                self.move()

        else:
            self.move()
