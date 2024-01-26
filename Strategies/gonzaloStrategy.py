from Strategies.strategy import Strategy
from constantes import *
import math
import random
from players.goalKeeper import GoalKeeper

class GonzaloStrategy(Strategy):
    def _init_(self):
        super()._init_()

    # modulo que devuelve true o false si mi equipo tiene la pelota o no
    def team_has_ball(self, player):
        teammates = player.mediator.getTeammates(player.team)
        for teammate in teammates:
            if teammate.hasBall:
                return True
        return False

    # modulo que devuelve true o false si el equipo rival tiene la pelota o no
    def rival_has_ball(self, player):
        rivals = player.mediator.getRivals(player.team)
        for rival in rivals:
            if rival.hasBall:
                return True
        return False

    # modulo que me dice si el jugador es el mas cercano a la pelota
    def is_closest(self, player):
        my_team = player.mediator.getTeammates(player.team)
        ball_x, ball_y = player.mediator.getBallsPosition()
        player_distance = self.distance((player.rect.centerx, player.rect.centery), (ball_x, ball_y))
        for teammate in my_team:
            if teammate != player or not isinstance(player, GoalKeeper):
                teammate_distance = self.distance((teammate.rect.centerx, teammate.rect.centery), (ball_x, ball_y))
                if player_distance > teammate_distance:
                    return False
        return True

    # modulo donde si soy el mas cercano a la pelota me muevo hacia ella, sino me muevo al rival mas cercano que este desmarcado
    def move_towards_ball(self, player):
        rivals = player.mediator.getRivals(player.team)
        closest_unmarked_rival = min(rivals, key=lambda r: (self.distance_to_player(r, player), not self.is_marked(r)))
        return self.one_on_one(player, closest_unmarked_rival)

    # modulo que me dice si alguien de mi equipo esta a menos de 4o de distancia de un rival (marcado)
    def is_marked(self, rival):
        teammates = rival.mediator.getRivals(rival.team)
        for teammate in teammates:
            if self.distance_to_player(rival, teammate) <= 40:
                return True
        return False

    # modulo que decide si el jugador debe moverse a marcar al rivar o debe mantenerse en el lugar
    def one_on_one(self, player, rival):
        distance_to_rival = self.distance_to_player(player, rival)
        marking_threshold = 100
        if distance_to_rival <= marking_threshold:
            return rival.rect.centerx, rival.rect.centery
        return player.rect.centerx + random.randint(-10,10), player.rect.centery + random.randint(-10,10)

    # modulo que 
    def player_movement_team_with_ball(self, player):
        if player.team:
            # si el jugador esta entre los limites inferiores y superiores del area se mueve hacia el area rival
            if AREA_G_SUP < player.rect.centery < AREA_G_INF:
                return AREA_G_MID_DER, player.rect.centery
            # si no se encuentra entre los limites del area se mueve un poco en diagonal y hacia adelante
            elif player.rect.centery < AREA_G_SUP:
                return AREA_G_MID_DER, PALO_SUP
            return AREA_G_MID_DER, PALO_INF
        else:
            # si el jugador esta entre los limites inferiores y superiores del area se mueve hacia el area rival
            if AREA_G_SUP < player.rect.centery < AREA_G_INF:
                return AREA_G_MID_IZQ, player.rect.centery
            # si no se encuentra entre los limites del area se mueve un poco en diagonal y hacia adelante
            elif player.rect.centery < AREA_G_SUP:
                return AREA_G_MID_IZQ, PALO_SUP
            return AREA_G_MID_IZQ, PALO_INF

    # se mueve entre los palos
    def move_goalkeeper(self, goalkeeper):
        ball_centerx, ball_centery = self.mediator.getBallsPosition()
        if ball_centery < PALO_SUP:
            return goalkeeper.rect.centerx, PALO_SUP
        elif ball_centery > PALO_INF:
            return goalkeeper.rect.centerx, PALO_INF
        return goalkeeper.rect.centerx, ball_centery
        

    def getProxPos(self, player):
        ball_x, ball_y = player.mediator.getBallsPosition()
        if isinstance(player, GoalKeeper):
            return self.move_goalkeeper(player)
        else:
            # movimiento si mi equipo tiene la pelota
            if self.team_has_ball(player):
                return self.player_movement_team_with_ball(player)
            # movimiento si es el jugador mas cercano a la pelota
            if self.is_closest(player):
                return ball_x, ball_y
            #movimiento si no es el jugador mas cercano a la pelota, va hacia el rival mas cercano
            return self.move_towards_ball(player)
            # sino es el mas cercano y esta suelta 
            return player.rect.centerx + random.randint(-10,10) , player.rect.centery + random.randint(-10,10)

    def with_ball(self, player):
        # si estoy en el area rival pateo
        if isinstance(player, GoalKeeper):
            return 2 # se puede hacer que se mueva pero el pase es lo mas facil
        else:
            if ((player.team==True) and (player.rect.centerx > (AREA_G_MID_DER - 250)) and (player.rect.centery>AREA_G_SUP) and (player.rect.centery<AREA_G_INF)) or ((player.team==False) and (player.rect.centerx < AREA_G_MID_IZQ + 250) and (player.rect.centery>AREA_G_SUP) and (player.rect.centery<AREA_G_INF)):
                return 1
            # si no estoy en el area, y no tengo rivales cerca avanzo, sino la paso al jugador mas cercano
            if self.no_rivals_near(player):
                return 3
            else:
                return 2
        
    # se la paso al compañero mas cercano aunque este marcado
    def where_to_pass(self,player):
        teammates = player.mediator.getTeammates(player.team)
        min_distance = float('inf')
        nearest_teammate = 0,0
        if player.team:
            nearest_teammate = FONDO_DER, player.rect.centery
        else:
            nearest_teammate = FONDO_IZQ, player.rect.centery
        for teammate in teammates:
            if(teammate!=player):
                actual_distance = self.distance_to_player(player,teammate)
                if(actual_distance<min_distance):
                    min_distance=actual_distance
                    nearest_teammate = teammate.rect.center
        return nearest_teammate
    
    def no_rivals_near(self, player):
        rivals = player.mediator.getRivals(player.team)
        for rival in rivals:
            if self.distance_to_player(player,rival) < 100:
                return False
        return True
    
    #distancia entre dos jugadores
    def distance_to_player(self, player1, player2):
        return math.sqrt((player2.rect.centerx - player1.rect.centerx)*2 + (player2.rect.centery - player1.rect.centery)*2)
    
    #distancia entre un jugador y la pelota
    def distance_to_ball(self, player, ball_centerx, ball_centery):
        return math.sqrt((ball_centerx - player.rect.centerx)*2 + (ball_centery - player.rect.centery)*2)
    
    #distancia entre dos puntos
    def distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0])*2 + (point2[1] - point1[1])*2)