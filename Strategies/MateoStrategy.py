from Strategies.strategy import Strategy
import math
from constantes import *
from players.goalKeeper import GoalKeeper
import random

class MateoStrategy(Strategy):
    MAX_DISTANCE_ALLOWED = 400
    def __init__(self):
        super().__init__()
        
    
    def myTeamHasBall(self,player):
        myTeam = player.mediator.getTeammates(player.team)
        for teammate in myTeam:
                if teammate.hasBall:
                    return True
        return False
    
    def RivalHasBall(self,player):
        rivals = player.mediator.getRivals(player.team)
        for rival in rivals:
                if rival.hasBall:
                    return True
        return False
    
    def isClosest(self, player):
        myTeam = player.mediator.getTeammates(player.team)
        ballx,bally = player.mediator.getBallsPosition()
        distancex = player.rect.centerx-ballx
        distancey = player.rect.centery-bally
        modulo= (distancex**2 + distancey**2)**(1/2)
        for teammate in myTeam:
            if teammate!= player or not isinstance(player, GoalKeeper):
                distancex1 = teammate.rect.centerx-ballx
                distancey1 = teammate.rect.centery-bally
                modulo1= (distancex1**2 + distancey1**2)**(1/2)
                if modulo> modulo1:
                    return False
        return True

    def rivalIsNear(self,player):
        rivals = player.mediator.getRivals(player.team)
        for rival in rivals:
            distx = abs(rival.rect.centerx - player.rect.centerx)
            disty = abs(rival.rect.centery - player.rect.centery)
            modulo = (distx**2 + disty**2)**(1/2)
            if modulo<50:
                return True
        return False
    
    def distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

    def distance_to_player(self, player1, player2):
        return self.distance((player1.rect.centerx, player1.rect.centery), (player2.rect.centerx, player2.rect.centery))

    def playerIsFree(self, player, destination_x, destination_y):
        rivals = player.mediator.getRivals(player.team)
        for rival in rivals:
            rx, ry = rival.rect.centerx, rival.rect.centery  
            # Verifica si el rival está en la trayectoria de pase
            if self.is_point_on_line(player.rect.centerx, player.rect.centery, destination_x, destination_y, rx, ry):
                return False
        # Si no hay rivales en la trayectoria de pase, el jugador está libre
        return True

    def is_point_on_line(self, x1, y1, x2, y2, px, py):
        # Utiliza una pequeña tolerancia (puedes ajustar según tus necesidades)
        tolerance = 5
        # Calcula la distancia entre el punto y la línea usando la fórmula de distancia punto-línea
        denominator = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        # Verifica si la distancia (denominador) es cercana a cero para evitar la división por cero
        if abs(denominator) < 1e-10:
            return abs(x2 - px) < tolerance and abs(y2 - py) < tolerance
        distance = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / denominator
        return distance < tolerance

    def distance_to_goal(self, player):
        if player.team:
            goal_position= (FONDO_DER,SAQUE)
        else:
            goal_position = (FONDO_IZQ, SAQUE)
        distance = math.hypot(goal_position[0] - player.rect.centerx, goal_position[1] -player.rect.centery)
        return distance

    
    def getClosestTeammate(self, player):
        myTeam = player.mediator.getTeammates(player.team)
        player_position = (player.rect.centerx, player.rect.centery)
        closest_teammate = None
        closest_distance = None
        for teammate in myTeam:
            if teammate != player:
                teammate_position = (teammate.rect.centerx, teammate.rect.centery)
                distance = self.distance(player_position, teammate_position)
                if closest_distance is None or distance < closest_distance:
                    closest_teammate = teammate
                    closest_distance = distance
        if closest_teammate is not None:
            return closest_teammate.rect.centerx - player.rect.centerx, closest_teammate.rect.centery - player.rect.centery
        else:
            return 0, 0
            

    def player_movement_rival_with_ball(self, player):
        px, py = player.mediator.getBallsPosition()
        x, y = player.rect.centerx, player.rect.centery
        rivals = player.mediator.getRivals(player)
        teammates = player.mediator.getTeammates(player)
        # Si el equipo es izquierdo y la pelota está en la mitad derecha
        if player.team and px > MITAD_CANCHA:
            if x > AREA_G_MID_IZQ:
                return x - random.uniform(1,5), y  
            else:
                return x + random.uniform(1,5), y      
        # Si el equipo es derecho y la pelota está en la mitad izquierda
        elif not player.team and px < MITAD_CANCHA:
            if x < AREA_G_MID_DER:
                return x + random.uniform(1,5), y  # Retroceder hacia la derecha
            else: 
                return x - random.uniform(1,5), y      # Avanzar hacia la izquierda
        # Si es el jugador más cercano a la pelota, seguir la pelota
        if self.isClosest(player):
            return px, py
        else: 
            # Verificar si el rival más cercano no está siendo marcado
            closest_unmarked_rival = min(rivals, key=lambda r: self.distance_to_player(r, player))
            if not self.is_being_marked(closest_unmarked_rival):
                return self.man_to_man_marking(player, closest_unmarked_rival)
            # Vuelvo en X tanto como lo haga la pelota, considerando el equipo
            if player.team:
                return x - (px - x), y  # Retroceder hacia la izquierda
            else:
                return x + (px - x), y  # Retroceder hacia la derecha

    def is_being_marked(self, rival):
        teammates= rival.mediator.getRivals(rival.team)
        for teammate in teammates:
            distance= self.distance_to_player(rival,teammate)
            if distance< 40:
                return True
        return False

    def man_to_man_marking(self, player, rival):
        # Calcular la distancia al rival objetivo
        distance_to_rival = self.distance_to_player(player, rival)
        #umbral para la marca personal
        marking_threshold = 50
        # Verificar si la distancia al rival está dentro del umbral para activar la marca personal
        if distance_to_rival <= marking_threshold:
            # Moverse hacia la posición del rival objetivo
            return rival.rect.centerx, rival.rect.centery
        return player.rect.centerx, player.rect.centery
    
    def player_movement_with_ball(self, player):
        y = player.rect.centery
        if player.hasBall:
            if player.team:
                return AREA_G_MID_DER, y
            else:
                return AREA_G_MID_IZQ, y
        if player.team:
            if player.rect.centery > AREA_G_INF:
                if player.rect.centerx < MITAD_CANCHA:
                    return player.rect.centerx+10, player.rect.centery
                elif player.rect.centerx < AREA_G_MID_DER-30:
                    return player.rect.centerx+10, player.rect.centery-5
                else:
                    return player.rect.centerx, player.rect.centery-10
            elif player.rect.centery < AREA_G_SUP:
                if player.rect.centerx < MITAD_CANCHA:
                    return player.rect.centerx+10, player.rect.centery
                elif player.rect.centerx < AREA_G_MID_DER-30:
                    return player.rect.centerx+10, player.rect.centery+5
                else:
                    return player.rect.centerx, player.rect.centery+10
            elif player.rect.centerx < AREA_G_MID_DER:
                return player.rect.centerx+10, player.rect.centery
            else:
                return player.rect.centerx-10, player.rect.centery
        else:
            if player.rect.centery > AREA_G_INF:
                if player.rect.centerx > MITAD_CANCHA:
                    return player.rect.centerx-10, player.rect.centery
                elif player.rect.centerx > AREA_G_MID_IZQ+30:
                    return player.rect.centerx-10, player.rect.centery-5
                else:
                    return player.rect.centerx, player.rect.centery-10
            elif player.rect.centery < AREA_G_SUP:
                if player.rect.centerx > MITAD_CANCHA:
                    return player.rect.centerx-10, player.rect.centery
                elif player.rect.centerx > AREA_G_MID_IZQ+30:
                    return player.rect.centerx-10, player.rect.centery+5
                else:
                    return player.rect.centerx, player.rect.centery+10
            elif player.rect.centerx > AREA_G_MID_IZQ:
                return player.rect.centerx-10, player.rect.centery
            else:
                return player.rect.centerx+10, player.rect.centery

    def move_goalkeeper(self, goalkeeper):
        # Definir un atributo booleano en el arquero
        if not hasattr(goalkeeper, 'moving_up'):
            goalkeeper.moving_up = True
        px, py = goalkeeper.mediator.getBallsPosition()
        # Distancia mínima para activar el movimiento hacia la pelota en el eje Y
        R = 150
        # Calcular la distancia entre el arquero y la pelota
        distancia_pelota = math.hypot(goalkeeper.rect.centerx - px, goalkeeper.rect.centery - py)
        # Verificar si la pelota está a una distancia menor o igual a R
        if self.isClosest(goalkeeper)and distancia_pelota<=250:
            return px,py
        elif distancia_pelota <= R:
            # Mover hacia la posición de la pelota en el eje Y
            if goalkeeper.rect.centery < py:
                return goalkeeper.rect.centerx, goalkeeper.rect.centery + 1  # Mover hacia abajo
            else:
                return goalkeeper.rect.centerx, goalkeeper.rect.centery - 1  # Mover hacia arriba
        else:
            if goalkeeper.rect.top <= PALO_SUP:
                goalkeeper.moving_up = False
            elif goalkeeper.rect.bottom >= PALO_INF:
                goalkeeper.moving_up = True
            if goalkeeper.team: 
                if goalkeeper.moving_up:
                    return FONDO_IZQ, goalkeeper.rect.top - 1  # Mover hacia arriba
                else:
                    return FONDO_IZQ, goalkeeper.rect.bottom + 1  # Mover hacia abajo
            else: 
                if goalkeeper.moving_up:
                    return FONDO_DER, goalkeeper.rect.top - 1  # Mover hacia arriba
                else:
                    return FONDO_DER, goalkeeper.rect.bottom + 1  # Mover hacia abajo  

    def getProxPos(self, player):
        px, py = player.mediator.getBallsPosition()
        if isinstance(player, GoalKeeper):
            return self.move_goalkeeper(player)
        else:
            #si mi equipo tiene la pelota
            myTeamHasBall = self.myTeamHasBall(player)
            if player.hasBall or myTeamHasBall:
                x,y= self.player_movement_with_ball(player)
                return x,y
            #si el rival tiene la pelota
            if self.RivalHasBall(player):
                return self.player_movement_rival_with_ball(player)
            #si la pelota esta suelta
            if self.isClosest(player):
                return px,py
        return player.rect.centerx + random.uniform(-10,10),player.rect.centery + random.uniform(-5,5)
            
    def with_ball(self, player):
        ballx,bally = player.mediator.getBallsPosition()
        if isinstance(player, GoalKeeper):
            return 2
        else:
            if player.rect.centerx==MITAD_CANCHA and ballx == MITAD_CANCHA and player.rect.centery==SAQUE and bally == SAQUE:
                return 2
            else:
                if self.distance_to_goal(player)<=self.MAX_DISTANCE_ALLOWED:
                    return 1
                if self.rivalIsNear(player):
                    return 2
            return 3
        
    def where_to_pass(self, player):
        teammates= player.mediator.getTeammates(player.team)
        # Elimina al jugador actual de la lista de compañeros ya que no vale auto-pase
        newteammates = [teammate for teammate in teammates if teammate != player and not isinstance(player, GoalKeeper)]
        for teammate in newteammates:
            x,y= teammate.rect.centerx, teammate.rect.centery
            #al primero que esté libre se la paso
            if self.playerIsFree(player,x,y):
                return x,y
        # por defecto tiro al arco
        if player.team:
            if player.rect.centerx<MITAD_CANCHA:
                if player.rect.centery<SAQUE:
                    return MITAD_CANCHA-10,LATERAL_IZQ
                else:
                    return MITAD_CANCHA-10,LATERAL_DER
            return FONDO_DER,SAQUE
        else:
            if player.rect.centerx>MITAD_CANCHA:
                if player.rect.centery<SAQUE:
                    return MITAD_CANCHA+10,LATERAL_IZQ
                else:
                    return MITAD_CANCHA+10,LATERAL_DER
            return FONDO_IZQ,SAQUE

    '''            
    def getFarthestTeammate(self, player):
        myTeam = player.mediator.getTeammates(player.team)
        player_position = (player.rect.centerx, player.rect.centery)
        farthest_teammate = None
        farthest_distance = 0
        for teammate in myTeam:
            if teammate != player:
                teammate_position = (teammate.rect.centerx, teammate.rect.centery)
                distance = self.distance(player_position, teammate_position)
                if farthest_teammate is None or distance > farthest_distance:
                    farthest_teammate = teammate
                    farthest_distance = distance
        if farthest_teammate is not None:
            return farthest_teammate.rect.centerx - player.rect.centerx, farthest_teammate.rect.centery - player.rect.centery
        else:
            return 0, 0

    
    '''