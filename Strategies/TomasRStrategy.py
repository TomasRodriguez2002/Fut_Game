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

    def isMyTeamWithBall(self, player):
        teammates = self.mediator.getTeammates(player.team)
        for teammate in teammates:
            if teammate != player and teammate.hasBall:
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
    
    def im_the_closest_to_the_area(self, player):
        teammates = self.mediator.getTeammates(player.team)
        if player.team:
            for teammate in teammates:
                if (teammate != player) and (not isinstance(teammate, GoalKeeper)) and \
                    (teammate.rect.centerx < player.rect.centerx):
                    return False
        else:
            for teammate in teammates:
                if (teammate != player) and (not isinstance(teammate, GoalKeeper)) and \
                    (teammate.rect.centerx > player.rect.centerx):
                    return False
        return True
    
    def im_the_furthest_from_the_area(self, player):
        teammates = self.mediator.getTeammates(player.team)
        if player.team:
            for teammate in teammates:
                if (teammate != player) and (not isinstance(teammate, GoalKeeper)) and \
                    (teammate.rect.centerx > player.rect.centerx):
                    return False
        else:
            for teammate in teammates:
                if (teammate != player) and (not isinstance(teammate, GoalKeeper)) and \
                    (teammate.rect.centerx < player.rect.centerx):
                    return False
        return True
    
    def im_the_closest_to_the_position(self, player, position):
        teammates = self.mediator.getTeammates(player.team)
        distance_to_position = (position[0] - player.rect.centerx)**2 + (position[1] - player.rect.centery)**2
        for teammate in teammates:
            if (teammate != player) and (not isinstance(teammate, GoalKeeper)):
                teammate_distance_to_position = (position[0] - teammate.rect.centerx)**2 + (position[1] - teammate.rect.centery)**2
                if teammate_distance_to_position < distance_to_position:
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
            '''
            # si la pelota esta dentro del area grande y soy el jugador más cercano a ella voy a buscarla
            if (AREA_G_SUP < ball_centery < AREA_G_INF) and (((player.team) and (ball_centerx < AREA_G_MID_IZQ)) or \
                ((not player.team) and (ball_centerx > AREA_G_MID_DER))):
                    if self.im_the_closest_to_the_ball(player):
                        return ball_centerx, ball_centery
            '''
            # (340 arriba y 420 abajo) si esta fuera del area en mi mitad de cancha
            if (player.team) and (AREA_G_MID_IZQ < ball_centerx < MITAD_CANCHA):
                if 420 > ball_centery:
                    if 340 < ball_centery:
                        return FONDO_IZQ+10, ball_centery
                    else:
                        return FONDO_IZQ+10, 340
                else:
                    return FONDO_IZQ+10, 420
                
            elif (not player.team) and (MITAD_CANCHA < ball_centerx < AREA_G_MID_DER):
                if 420 > ball_centery:
                    if 340 < ball_centery:
                        return FONDO_DER-10, ball_centery
                    else:
                        return FONDO_DER-10, 340
                else:
                    return FONDO_DER-10, 420

            # movimiento del arquero (pelota en mi mitad de cancha)
            if (player.team) and (ball_centerx <= AREA_G_MID_IZQ):
                if PALO_INF > ball_centery:
                    if PALO_SUP < ball_centery:
                        return FONDO_IZQ+10, ball_centery
                    else:
                        return FONDO_IZQ+10, PALO_SUP+14
                else:
                    return FONDO_IZQ+10, PALO_INF-14
                
            elif (not player.team) and (ball_centerx >= AREA_G_MID_DER):
                if PALO_INF > ball_centery:
                    if PALO_SUP < ball_centery:
                        return FONDO_DER-10, ball_centery
                    else:
                        return FONDO_DER-10, PALO_SUP+14
                else:
                    return FONDO_DER-10, PALO_INF-14
                
            # movimiento del arquero (pelota en mitad de cancha rival)
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

            if player.hasBall or self.isMyTeamWithBall(player): 
                if player.team:

                    # si la pelota la tiene un compañero, no yo, voy a marcar al contrincante que esta en mi area
                    if not player.hasBall:

                        # si hay un contrincante en mi area lo marco
                        rival = self.there_is_a_rival_in_my_area(player.team)
                        if rival != None:
                            return rival.rect.centerx, rival.rect.centery
                        
                        # para no dejar al arquero solo, uno se queda abajo
                        if self.im_the_closest_to_the_area(player):
                            if player.team:
                                return POS_P8_F5
                            return POS_P3_F5

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
                        
                    # central se queda en su lugar, si tiene la pelota avanza
                    elif player.rect.centerx < MITAD_CANCHA:
                        #if player.hasBall:
                            return AREA_G_MID_DER, player.rect.centery
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)
                    
                    # enganche avanza en x
                    elif player.rect.centerx < AREA_G_MID_DER-100:
                        return AREA_G_MID_DER-100, player.rect.centery
                    
                    # nueve se queda en el area (moviendose en y)
                    else:
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)

                else:

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
                        if player.hasBall:
                            return AREA_G_MID_IZQ, player.rect.centery
                        return player.rect.centerx + random.randint(-10, 10), player.rect.centery + random.randint(-10, 10)

                    # enganche avanza en x
                    elif player.rect.centerx > AREA_G_MID_IZQ+100:
                        return AREA_G_MID_IZQ+100, player.rect.centery
                    
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
                    
                    # si soy el mas cercano a mi area me quedo abajo para ayudar al arquero
                    if self.im_the_closest_to_the_area(player):
                        return POS_P8_F5
                    
                    # si soy el mas lejano al area me posiciono como enganche para esperar la pelota cerca de mitad de cancha
                    if self.im_the_furthest_from_the_area(player):
                        return POS_P6_F5

                    # si estoy en la banda izq me posiciono como lateral izq
                    if player.rect.centery < SAQUE:
                        # si somos dos en la misma banda, si soy el mas cercano a la posicion P7 voy hacia ella
                        if self.im_the_closest_to_the_position(player, POS_P7_F5):
                            return POS_P7_F5
                    # si estoy en la banda der me posiciono como lateral der
                    return POS_P9_F5

                    '''
                    # si estoy fuera del area grande retrocedo
                    if player.rect.centerx > AREA_G_MID_IZQ:
                        return AREA_G_MID_IZQ, player.rect.centery
                    # sino me quedo al borde del area
                    return player.rect.centerx, player.rect.centery + random.randint(-10, 10)
                    '''
                
                # si los rivales estan en su mitad de cancha con la pelota
                elif (not player.team) and (ball_centerx < MITAD_CANCHA):

                    # si soy el mas cercano a mi area me quedo abajo para ayudar al arquero
                    if self.im_the_closest_to_the_area(player):
                        return POS_P3_F5
                    
                    # si soy el mas lejano al area me posiciono como enganche para esperar la pelota cerca de mitad de cancha
                    if self.im_the_furthest_from_the_area(player):
                        return POS_P1_F5

                    # si estoy en la banda izq me posiciono como lateral izq
                    if player.rect.centery < SAQUE:
                        # si somos dos en la misma banda, si soy el mas cercano a la posicion P2 voy hacia ella
                        if self.im_the_closest_to_the_position(player, POS_P2_F5):
                            return POS_P2_F5
                    # si estoy en la banda der me posiciono como lateral der
                    return POS_P4_F5
                
                    '''
                    # si estoy fuera del area grande retrocedo
                    if player.rect.centerx < AREA_G_MID_DER:
                        return AREA_G_MID_DER, player.rect.centery
                    # sino me quedo al borde del area
                    return player.rect.centerx, player.rect.centery + random.randint(-10, 10)
                    '''

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

            # si la pelota esta suelta en mi area y no soy el mas cercano a ella
            if ((player.team) and (ball_centerx < MITAD_CANCHA)) or ((not player.team) and (ball_centerx > MITAD_CANCHA)):     
                # marco al rival mas cercano que no este siendo marcado por un compañero (codigo repetido) 
                return self.mark_the_nearest_player_not_marked_by_a_teammate(player)

            # si la pelota esta en el area rival y soy el mas cercano a mi area me quedo abajo para ayudar al arquero
            if self.im_the_closest_to_the_area(player):
                if player.team:
                    return POS_P8_F5
                return POS_P3_F5

            # estoy en mitad de cancha de mi equipo -> en funcion de la banda donde este hago de punta hasta mitad de cancha
            if ((player.team) and (player.rect.centerx < MITAD_CANCHA)): 
                # punta izq
                if player.rect.centery < SAQUE:
                    if self.im_the_closest_to_the_position(player, POS_P7_F5):
                        return MITAD_CANCHA, POS_P7_F5[1] 
                # punta der
                return MITAD_CANCHA, POS_P9_F5[1]
            
            if ((not player.team) and (player.rect.centerx > MITAD_CANCHA)):
                # punta izq
                if player.rect.centery < SAQUE:
                    if self.im_the_closest_to_the_position(player, POS_P2_F5):
                        return MITAD_CANCHA, POS_P2_F5[1] 
                # punta der
                return MITAD_CANCHA, POS_P4_F5[1]
            
            # pelota suelta y estoy en mitad de cancha rival al igual que la pelota
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
        for teammate in teammates:
            for rival in rivals:
                if teammate != player:
                    
                    if (((player.team) and (teammate.rect.centerx <= rival.rect.centerx)) or \
                    ((not player.team) and (teammate.rect.centerx >= rival.rect.centerx+40))) and \
                    (self.distance_to_player(teammate, rival) > 30):
                        return teammate.rect.centerx, teammate.rect.centery
                    '''
                    # verificar que el jugador no este a la espalda del rival para evitar pases al rival
                    # (en funcion de si estoy delante o detras de mi compañero cambia la perspectiva de su espalda)
                    if self.distance_to_player(teammate, rival) >= 40:
                    '''
        # como estoy en mi mitad de cancha, por defecto se la paso al arquero
        if not isinstance(player, GoalKeeper):
            
            # en nuestra area no se la paso al arquero para evitar gol en contra
            if (player.rect.centerx < AREA_G_MID_IZQ) or (player.rect.centerx > AREA_G_MID_DER):
                # lateral izq -> pase filtrado hacia adelante
                if player.rect.centery < AREA_G_SUP:
                    x, y = MITAD_CANCHA, AREA_G_SUP
                # lateral der -> pase filtrado hacia adelante
                elif player.rect.centery > AREA_G_INF:
                    x, y = MITAD_CANCHA, AREA_G_INF
                # central revienta hacia arriba o hacia abajo
                else:
                    x, y = player.rect.centerx, random.choice([LATERAL_DER, LATERAL_IZQ])
            
            # en mitad de cancha rival tampoco, esta muy lejos y se la puedo regalar al rival
            elif ((player.team) and (player.rect.centerx > MITAD_CANCHA)) or \
                ((not player.team) and (player.rect.centerx < MITAD_CANCHA)):
                # en banda izq la filtro hacia el arco
                if player.rect.centery < AREA_C_SUP:
                    if player.team:
                        return AREA_G_MID_DER, AREA_C_SUP
                    return AREA_G_MID_IZQ, AREA_C_SUP
                # en banda izq la filtro hacia el arco
                if player.rect.centery > AREA_C_INF:
                    if player.team:
                        return AREA_G_MID_DER, AREA_C_INF
                    return AREA_G_MID_IZQ, AREA_C_INF
                # en el centro la filtro hacia alguna banda
                if player.team:
                    return AREA_G_MID_DER, random.choice([AREA_G_SUP, AREA_G_INF])
                return AREA_G_MID_IZQ, random.choice([AREA_G_SUP, AREA_G_INF])

            else:
                i = 0
                flag = False
                while (i < len(teammates) and (not flag)):
                    teammate = teammates.sprites()[i]
                    if(isinstance(teammate, GoalKeeper)):
                        flag = True
                        x, y = teammate.rect.centerx, teammate.rect.centery
                    i += 1
        # si soy el arquero, por defecto la despejo hacia arriba o hacia abajo
        else:
            x, y = player.rect.centerx, random.choice([LATERAL_IZQ, LATERAL_DER])

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