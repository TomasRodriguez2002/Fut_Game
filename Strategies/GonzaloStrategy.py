from Strategies.Strategy import Strategy
import math
from Constantes import *

class GonzaloStrategy(Strategy):
    def __init__(self):
        super().__init__()
    
    def getProxPos(self, player):
        return 3

    def with_ball(self, player):
        # si estoy en el area rival pateo
        if ((player.team==True) and (player.rect.centerx > AREA_G_MID_DER) and (player.rect.centery<AREA_C_SUP) and (player.rect.centery>AREA_C_INF)) or ((player.team==False) and (player.rect.centerx < AREA_G_MID_IZQ) and (player.rect.centery<AREA_C_SUP) and (player.rect.centery>AREA_C_INF)):
            return 1
        # si no estoy en el area, la paso
        return 2
        
    # se la paso al compañero mas cercano
    def where_to_pass(self,player):
        teammates = player.mediator.getTeammates(player.team)
        min_distance = float('inf')
        nearest_teammate = None
        for teammate in teammates:
            if(teammate!=player):
                actual_distance = self.distance_to_player(self,player,teammate)
                if(actual_distance<min_distance):
                    min_distance=actual_distance
                    nearest_teammate = teammate
        return nearest_teammate
    
    #distancia entre dos jugadores
    def distance_to_player(self, player1, player2):
        return math.sqrt((player2.rect.centerx - player1.rect.centerx)**2 + (player2.rect.centery - player1.rect.centery)**2)
    
    #distancia entre un jugador y la pelota
    def distance_to_ball(self, player, ball_centerx, ball_centery):
        return math.sqrt((ball_centerx - player.rect.centerx)**2 + (ball_centery - player.rect.centery)**2)