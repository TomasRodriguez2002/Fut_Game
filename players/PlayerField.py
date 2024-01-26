from hmac import new

from players.player import Player
from constantes import *

class PlayerField(Player):
    def __init__(self, spritePNG, strategy, mediator, team):
        super().__init__(spritePNG, strategy, mediator, team)

    def move(self):
        target_x, target_y = self.strategy.getProxPos(self)

        new_x, new_y = self.calculate_new_pos(target_x, target_y)

        # Verificar límites laterales y de fondo
        if LATERAL_IZQ - 7 < new_y < LATERAL_DER - self.rect.height + 7 and \
            FONDO_IZQ - 5 < new_x < FONDO_DER - self.rect.width + 5:
            # Verificar la distancia con los compañeros
            #if self.mediator.can_move(self.team, new_x, new_y):
            # if self.mediator.can_move(self.team, self):
            self.animation_of_move()

    def update(self):
        
        #si la distancia entre el jugador y la pelota es menor que 20 entonces el jugador tiene la pelota
        #super.mediator.check_collision_with_ball(self)
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


