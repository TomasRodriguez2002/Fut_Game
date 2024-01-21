from Strategies.Strategy import Strategy
import math, random
from Constantes import *
from players.GoalKeeper import GoalKeeper

class TomasRStrategy(Strategy):

    # 27 px de width y height el sprite del player

    MARKS_DISTANCE = 80
    CONSIDERABLE_DISTANCE_TO_MARK = 120

    def __init__(self):
        super().__init__()

    def isMyTeamWithBall(self, team):
        teammates = self.mediator.getTeammates(team)
        for teammate in teammates:
            if teammate.hasBall:
                return True
        return False
    
    def isMyrivalTeamWithBall(self, team):
        rivals = self.mediator.getRivals(team)
        for rival in rivals:
            if rival.hasBall:
                return True
        return False

    def isMyTeamWithoutBall(self, team):
        teammates = self.mediator.getTeammates(team)
        for teammate in teammates:
            if teammate.hasBall:
                return False
        return True

    def isMyRivalTeamWithoutBall(self, team):
        rivals = self.mediator.getRivals(team)
        for rival in rivals:
            if rival.hasBall:
                return False
        return True
    
    def im_the_closest_to_the_ball(self, player):
        ball_centerx, ball_centery = self.mediator.getBallsPosition()
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)
        for rival in rivals:
            if self.distance_to_ball(rival, ball_centerx, ball_centery) < self.distance_to_ball(player, ball_centerx, ball_centery):
                return False
        for teammate in teammates:
            if self.distance_to_ball(teammate, ball_centerx, ball_centery) < self.distance_to_ball(player, ball_centerx, ball_centery):
                return False
        return True
    
    def distance_to_player(self, player1, player2):
        return math.sqrt((player2.rect.centerx - player1.rect.centerx)**2 + (player2.rect.centery - player1.rect.centery)**2)
    
    def distance_to_ball(self, player, ball_centerx, ball_centery):
        return math.sqrt((ball_centerx - player.rect.centerx)**2 + (ball_centery - player.rect.centery)**2)

    def mark_the_nearest_player_not_marked_by_a_teammate(self, player):    
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)
        distance_to_rival = 0
        min_distance_to_rival = float('inf')
        # por defecto me quedo en mi posicion actual
        x, y = player.rect.centerx, player.rect.centery + random.randint(-10, 10)
        for rival in rivals:
            if not isinstance(rival, GoalKeeper):
                distance_to_rival = self.distance_to_player(player, rival)
                # Verificar si es el rival mas cercano y si eres el jugador más cercano entre tus compañeros a el
                if distance_to_rival < min_distance_to_rival and all(self.distance_to_player(teammate, rival) > \
                    distance_to_rival for teammate in teammates if teammate != player \
                    and not isinstance(teammate, GoalKeeper)):
                    x, y = rival.rect.centerx, rival.rect.centery
                    min_distance_to_rival = distance_to_rival
        return x, y
    
    def im_the_only_one_down(self, player):
        teammates = self.mediator.getTeammates(player.team)
        if player.team:
            for teammate in teammates:
                if teammate != player and not isinstance(teammate, GoalKeeper) and teammate.rect.centerx < MITAD_CANCHA:
                    return False
        else:
            for teammate in teammates:
                if teammate != player and not isinstance(teammate, GoalKeeper) and teammate.rect.centerx > MITAD_CANCHA:
                    return False
        return True
    
    def there_is_a_rival_in_my_area(self, team):
        rivals = self.mediator.getRivals(team)
        if team:
            for rival in rivals:
                if rival.rect.centerx < MITAD_CANCHA:
                    return rival
        else:
            for rival in rivals:
                if rival.rect.centerx > MITAD_CANCHA:
                    return rival
        return None

    def getProxPos(self, player):
        ball_centerx, ball_centery = self.mediator.getBallsPosition()
        if isinstance(player, GoalKeeper):

            # si la pelota esta dentro del area grande y soy el jugador más cercano a ella voy a buscarla
            if (AREA_G_SUP < ball_centery < AREA_G_INF) and (((player.team) and (ball_centerx < AREA_G_MID_IZQ)) or \
                ((not player.team) and (ball_centerx > AREA_G_MID_DER))):
                    if self.im_the_closest_to_the_ball(player):
                        return ball_centerx, ball_centery

            # movimiento del arquero (pelota en area grande)
            if (player.team) and (ball_centerx < AREA_C_MID_IZQ+200):
                if PALO_INF > ball_centery:
                    if PALO_SUP < ball_centery:
                        return FONDO_IZQ+10, ball_centery
                    else:
                        return FONDO_IZQ+10, PALO_SUP
                else:
                    return FONDO_IZQ+10, PALO_INF
            elif (not player.team) and (ball_centerx > AREA_C_MID_DER-200):
                if PALO_INF > ball_centery:
                    if PALO_SUP < ball_centery:
                        return FONDO_DER-10, ball_centery
                    else:
                        return FONDO_DER-10, PALO_SUP
                else:
                    return FONDO_DER-10, PALO_INF
                
            # movimiento del arquero (pelota fuera del area grande)
            if (player.team):
                if PALO_INF > ball_centery:
                    if PALO_SUP < ball_centery:
                        return AREA_C_MID_IZQ, ball_centery
                    else:
                        return AREA_C_MID_IZQ, PALO_SUP
                else:
                    return AREA_C_MID_IZQ, PALO_INF

            else:
                if PALO_INF > ball_centery:
                    if PALO_SUP < ball_centery:
                        return AREA_C_MID_DER, ball_centery
                    else:
                        return AREA_C_MID_DER, PALO_SUP
                else:
                    return AREA_C_MID_DER, PALO_INF
                
        # logica de jugador de campo
        else:
            
            if player.hasBall or self.isMyTeamWithBall(player.team): 
                if player.team:

                    '''
                    # si soy el unico abajo me quedo a defender
                    if (player.rect.centerx < MITAD_CANCHA and self.im_the_only_one_down(player)):
                        return AREA_G_MID_DER+100, SAQUE
                    '''

                    '''PUEDO COLOCAR A UN JUGADOR ABAJO PARA ACOMPAÑAR AL ARQUERO USANDO UN ATRIBUTO BOOLEANO
                        QUE INDIQUE QUE UN JUGADOR SE DIRIGE AL CENTRO, SI ES FALSE HACE ESO SINO SIGUE FLUJO NORMAL'''

                    # si hay un contrincante en mi area lo marco
                    rival = self.there_is_a_rival_in_my_area(player.team)
                    if rival != None:
                        return rival.rect.centerx, rival.rect.centery

                    # punta lateral derecho o izquierdo
                    if (player.rect.centery > AREA_C_INF) or (player.rect.centery < AREA_C_SUP):
                        # punta abajo avanza en x
                        if player.rect.centerx < MITAD_CANCHA:
                            return AREA_G_MID_DER, player.rect.centery
                        # punta arriba se adentra al area rival
                        elif player.rect.centerx < AREA_G_MID_DER:
                            return AREA_G_MID_DER, SAQUE
                        # punta en area rival (en coord x) sube hacia el arco
                        else:
                            return player.rect.centerx, SAQUE
                        
                    # central se queda en su lugar
                    elif player.rect.centerx < MITAD_CANCHA:
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)
                    
                    # enganche avanza en x
                    elif player.rect.centerx < AREA_G_MID_DER:
                        return AREA_G_MID_DER, player.rect.centery
                    
                    # nueve se queda en el area (moviendose en y)
                    else:
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)

                else:

                    '''
                    # si soy el unico abajo me quedo a defender
                    if (player.rect.centerx > MITAD_CANCHA and self.im_the_only_one_down(player)):
                        return AREA_G_MID_IZQ-100, SAQUE
                    '''

                    # punta lateral derecho o izquierdo
                    if (player.rect.centery > AREA_C_INF) or (player.rect.centery < AREA_C_SUP):
                        # punta abajo avanza en x
                        if player.rect.centerx > MITAD_CANCHA:
                            return AREA_G_MID_IZQ, player.rect.centery
                        # punta arriba se adentra al area rival
                        elif player.rect.centerx > AREA_G_MID_IZQ:
                            return AREA_G_MID_IZQ, SAQUE
                        # punta en area rival (en coord x) sube hacia el arco
                        else:
                            return player.rect.centerx, SAQUE
                        
                    # central se queda en su lugar
                    elif player.rect.centerx > MITAD_CANCHA:
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)

                    # enganche avanza en x
                    elif player.rect.centerx > AREA_G_MID_IZQ:
                        return AREA_G_MID_IZQ, player.rect.centery
                    
                    # nueve se queda en el area (moviendose en y)
                    else:
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)

            # si el equipo rival tiene la pelota 
            if self.isMyrivalTeamWithBall(player.team):
                
                # si no estoy a la espalda del rival que tiene la pelota
                if ((player.team) and (ball_centerx > player.rect.centerx)) or ((not player.team) and (ball_centerx < player.rect.centerx)):
                    distance_to_ball = self.distance_to_ball(player, ball_centerx, ball_centery)
                    # si la pelota no esta muy lejos voy a marcarlo en caso de ser el mas cercano al rival con la pelota (logica repetida abajo)
                    if distance_to_ball < self.CONSIDERABLE_DISTANCE_TO_MARK:
                        teammates = self.mediator.getTeammates(player.team)
                        distance_from_ball_to_teammate = 0
                        min_distance_from_ball_to_teammate = float('inf')
                        for teammate in teammates:
                            # no considero al arquero como candidato a ir a buscar la pelota, le dije que no vaya
                            if teammate != player and not isinstance(teammate, GoalKeeper):
                                distance_from_ball_to_teammate = self.distance_to_ball(teammate, ball_centerx, ball_centery)
                                if distance_from_ball_to_teammate < min_distance_from_ball_to_teammate:
                                    min_distance_from_ball_to_teammate = distance_from_ball_to_teammate
                        # soy el mas cercano -> voy a buscar la pelota
                        if (min_distance_from_ball_to_teammate > distance_to_ball):
                            return ball_centerx, ball_centery

                # si los rivales estan en su mitad de cancha con la pelota
                if (player.team) and (ball_centerx > MITAD_CANCHA):
                    # si estoy fuera del area grande retrocedo
                    if player.rect.centerx > AREA_G_MID_IZQ:
                        return AREA_G_MID_IZQ, player.rect.centery
                    # sino me quedo al borde del area
                    return player.rect.centerx, player.rect.centery + random.randint(-10, 10)
                
                # si los rivales estan en su mitad de cancha con la pelota
                elif (not player.team) and (ball_centerx < MITAD_CANCHA):
                    # si estoy fuera del area grande retrocedo
                    if player.rect.centerx < AREA_G_MID_DER:
                        return AREA_G_MID_DER, player.rect.centery
                    # sino me quedo al borde del area
                    return player.rect.centerx, player.rect.centery + random.randint(-10, 10)

                # en la mitad de cancha de mi equipo marco al juagador de campo rival mas cercano que no este
                # siendo marcado por un compañero
                return self.mark_the_nearest_player_not_marked_by_a_teammate(player)
                            
            ''' si la pelota esta suelta (ningun jugador tiene posesión de ella)'''
            # Chequear si algún compañero está más cerca de la pelota, sino voy yo a por ella
            teammates = self.mediator.getTeammates(player.team)
            distance_from_ball_to_teammate = 0
            min_distance_from_ball_to_teammate = float('inf')
            for teammate in teammates:
                # no considero al arquero como candidato a ir a buscar la pelota, le dije que se quedara quieto
                if teammate != player and not isinstance(teammate, GoalKeeper):
                    distance_from_ball_to_teammate = self.distance_to_ball(teammate, ball_centerx, ball_centery)
                    if distance_from_ball_to_teammate < min_distance_from_ball_to_teammate:
                        min_distance_from_ball_to_teammate = distance_from_ball_to_teammate
            # Si soy el jugador de mi equipo que se encuentra más cerca de la pelota voy hacia ella
            if min_distance_from_ball_to_teammate > self.distance_to_ball(player, ball_centerx, ball_centery):
                return ball_centerx, ball_centery

            # sino, mientras mi compañero va a buscar la pelota:      
            # si la pelota esta en mi area marco al rival mas cercano que no este siendo marcado por un compañero (codigo repetido) 
            
            if ((player.team) and (ball_centerx < MITAD_CANCHA)) or ((not player.team) and (ball_centerx > MITAD_CANCHA)):     
                return self.mark_the_nearest_player_not_marked_by_a_teammate(player)

            # si esta suelta en area rival y no soy el mas cercano para ir a buscarla me quedo en mi lugar
            #return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)

            # estoy en mitad de cancha de mi equipo y la pelota no esta a mi espalda -> avanzo
            if ((player.team) and (ball_centerx > player.rect.centerx) and (player.rect.centerx < MITAD_CANCHA)) or \
                ((not player.team) and (ball_centerx < player.rect.centerx) and (player.rect.centerx > MITAD_CANCHA)):
                    return MITAD_CANCHA, player.rect.centery
            # sino me quedo en el lugar
            return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)


    # retorna si un jugador esta siendo o no marcado
    def marked_player(self, player):
        rivals = self.mediator.getRivals(player.team)
        for rival in rivals:
            # se considera marcado si el rival se encuentra en frente
            if ((player.team) and (player.rect.centerx < rival.rect.centerx)) or \
                ((not player.team) and (player.rect.centerx > rival.rect.centerx)):
                    if self.distance_to_player(player, rival) < self.MARKS_DISTANCE:
                        return True
        return False

    # 1 -> patear | 2 -> pasar | 3 -> moverse
    def with_ball(self, player):
        
        if isinstance(player, GoalKeeper):
            return 2
        
        # si estoy en el area grande rival pateo
        if (player.team) and (player.rect.centerx > AREA_G_MID_DER-150) and (AREA_C_SUP < player.rect.centery < AREA_C_INF) or \
            (not player.team) and (player.rect.centerx < AREA_G_MID_IZQ+150) and (AREA_C_SUP < player.rect.centery < AREA_C_INF):
                return 1
        
        # si no puedo patear chequeo si tengo marca (la paso, sino me muevo hacia el area rival)
        if self.marked_player(player):
            return 2
        return 3

    # retorna la posicion del primer compañero que encuentre que tenga lejos la marca
    def find_the_furthest_player(self, player, teammates, rivals):
        x, y = 0, 0
        # como estoy en mi mitad de cancha, por defecto se la paso al arquero
        if not isinstance(player, GoalKeeper):
            i = 0
            flag = False
            while (i < len(teammates) and (not flag)):
                teammate = teammates.sprites()[i]
                if(isinstance(teammate, GoalKeeper)):
                    flag = True
                    x, y = teammate.rect.centerx, teammate.rect.centery
                i += 1
        # si soy el arquero, por defecto la despejo hacia arriba
        else:
            x, y = MITAD_CANCHA, LATERAL_IZQ
        
        for teammate in teammates:
            for rival in rivals:
                if teammate != player:
                    # verificar que el jugador no este a la espalda del rival para evitar pases al rival
                    if (((player.team) and (teammate.rect.centerx < rival.rect.centerx)) or \
                    ((not player.team) and (teammate.rect.centerx > rival.rect.centerx+40))) and \
                    (self.distance_to_player(teammate, rival) > 40):
                        return teammate.rect.centerx, teammate.rect.centery
        return x, y

    def where_to_pass(self, player):
        teammates = self.mediator.getTeammates(player.team)
        
        #if ((player.team) and (player.rect.centerx <= MITAD_CANCHA)) or ((not player.team) and (player.rect.centerx >= MITAD_CANCHA)):
        # se la paso primer compañero que considere que tiene la marca alejada
        rivals = self.mediator.getRivals(player.team)
        return self.find_the_furthest_player(player, teammates, rivals)
        '''
        # sino se la paso al compañero que este mas cerca del arco
        # por defecto pateo al arco
        x, y = 0, 0
        if player.team:
            x, y = FONDO_DER, random.randint(PALO_SUP - 20, PALO_INF + 20)
        else:
            x, y = FONDO_IZQ, random.randint(PALO_SUP - 20, PALO_INF + 20)
        pos_x_teammate = 0
        max_pos_x_teammate = -1
        for teammate in teammates:
            pos_x_teammate = teammate.rect.centerx
            if pos_x_teammate > max_pos_x_teammate:
                max_pos_x_teammate = pos_x_teammate
                x, y = teammate.rect.centerx, teammate.rect.centery
        return x, y
        '''