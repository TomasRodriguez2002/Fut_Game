from Strategies.Strategy import Strategy
import math, random
from Constantes import *
from players.GoalKeeper import GoalKeeper

class TomasRStrategy(Strategy):

    # 27 px de width y height el sprite del player

    MARKS_DISTANCE = 80

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
            if (math.sqrt((ball_centerx - rival.rect.centerx)**2 + (ball_centery - rival.rect.centery)**2)) < \
                (math.sqrt((ball_centerx - player.rect.centerx)**2 + (ball_centery - player.rect.centery)**2)):
                return False
        for teammate in teammates:
            if (math.sqrt((ball_centerx - teammate.rect.centerx)**2 + (ball_centery - teammate.rect.centery)**2)) < \
                (math.sqrt((ball_centerx - player.rect.centerx)**2 + (ball_centery - player.rect.centery)**2)):
                return False
        return True
    
    def distance_to_player(self, player1, player2):
        return math.sqrt((player2.rect.centerx - player1.rect.centerx)**2 + (player2.rect.centery - player1.rect.centery)**2)
    
    def distance_to_ball(self, player, ball_centerx, ball_centery):
        return math.sqrt((ball_centerx - player.rect.centerx)**2 + (ball_centery - player.rect.centery)**2)
    
    def marked_player(self, player):
        rivals = self.mediator.getRivals(player.team)
        for rival in rivals:
            # se considera marcado si el rival se encuentra en frente
            if ((player.team) and (player.rect.centerx < rival.rect.centerx)) or \
                ((not player.team) and (player.rect.centerx > rival.rect.centerx)):
                    if self.distance_to_player(player, rival) < self.MARKS_DISTANCE:
                        return True
        return False

    def getProxPos(self, player):
        ball_centerx, ball_centery = self.mediator.getBallsPosition()
        if isinstance(player, GoalKeeper):
            # si la pelota esta dentro del area grande y soy el jugador más cercano a ella voy a buscarla
            if player.team:
                if (ball_centerx < AREA_G_MID_IZQ) and (AREA_G_SUP < ball_centery < AREA_G_INF):
                    if self.im_the_closest_to_the_ball(player):
                        return ball_centerx, ball_centery
            else:
                if (ball_centerx > AREA_G_MID_DER) and (AREA_G_SUP < ball_centery < AREA_G_INF):
                    if self.im_the_closest_to_the_ball(player):
                        return ball_centerx, ball_centery
                    
            # movimiento del arquero (pelota dentro del area grande)
            if player.team:
                if ball_centerx < AREA_G_MID_IZQ:
                    if 420 > ball_centery:
                        if 340 < ball_centery:
                            return (FONDO_IZQ+10, SAQUE)
                        else:
                            return FONDO_IZQ+10, 340
                    else:
                        return FONDO_IZQ+10, 420
            else:
            # movimiento del arquero (pelota dentro del area grande)
                if ball_centerx > AREA_G_MID_DER:
                    if 420 > ball_centery:
                        if 340 < ball_centery:
                            return (FONDO_DER-10, SAQUE)
                        else:
                            return FONDO_DER-10, 340
                    else:
                        return FONDO_DER-10, 420
            if self.isMyTeamWithBall(player.team):
                if player.team:
                    # movimiento del arquero (pelota en area rival)
                    if ball_centerx > MITAD_CANCHA:
                        if AREA_C_INF > ball_centery:
                            if AREA_C_SUP < ball_centery:
                                return (AREA_G_MID_IZQ - player.rect.width + 4), ball_centery
                            else:
                                return (AREA_G_MID_IZQ - player.rect.width + 4), AREA_C_SUP
                        else:
                            return (AREA_G_MID_IZQ - player.rect.width + 4), AREA_C_INF
                    # movimiento del arquero (pelota fuera del area grande)
                    elif ball_centerx > AREA_G_MID_IZQ:
                        if PALO_INF > ball_centery:
                            if PALO_SUP < ball_centery:
                                return AREA_C_MID_IZQ, ball_centery
                            else:
                                return AREA_C_MID_IZQ, PALO_SUP
                        else:
                            return AREA_C_MID_IZQ, PALO_INF
                else:
                    # movimiento del arquero (pelota en area rival)
                    if ball_centerx < MITAD_CANCHA:
                        if AREA_C_INF > ball_centery:
                            if AREA_C_SUP < ball_centery:
                                return (AREA_G_MID_DER - 5), ball_centery
                            else:
                                return (AREA_G_MID_DER - 5), AREA_C_SUP
                        else:
                            return (AREA_G_MID_DER - 5), AREA_C_INF
                    # movimiento del arquero (pelota fuera del area grande)
                    elif ball_centerx < AREA_G_MID_DER:
                        if PALO_INF > ball_centery:
                            if PALO_SUP < ball_centery:
                                return AREA_C_MID_DER, ball_centery
                            else:
                                return AREA_C_MID_DER, PALO_SUP
                        else:
                            return AREA_C_MID_DER, PALO_INF
            # Rival tiene la pelota
            else:
                # movimiento del arquero (pelota en area rival). Misma logica que si mi equipo tiene la pelota
                # y se encuentra fuera del area grande (MODULARIZAR)
                if player.team:
                    if ball_centerx > MITAD_CANCHA:
                        if PALO_INF > ball_centery:
                            if PALO_SUP < ball_centery:
                                return AREA_C_MID_IZQ, ball_centery
                            else:
                                return AREA_C_MID_IZQ, PALO_SUP
                        else:
                            return AREA_C_MID_IZQ, PALO_INF
                    else:
                        # movimiento del arquero (pelota dentro o fuera del area grande)
                        if 420 > ball_centery:
                            if 340 < ball_centery:
                                return (FONDO_IZQ+10, SAQUE)
                            else:
                                return FONDO_IZQ+10, 340
                        else:
                            return FONDO_IZQ+10, 420
                else:
                    if ball_centerx < MITAD_CANCHA:
                        if PALO_INF > ball_centery:
                            if PALO_SUP < ball_centery:
                                return AREA_C_MID_DER, ball_centery
                            else:
                                return AREA_C_MID_DER, PALO_SUP
                        else:
                            return AREA_C_MID_DER, PALO_INF
                    else:
                        # movimiento del arquero (pelota en dentro o fuera del area grande)
                        if 420 > ball_centery:
                            if 340 < ball_centery:
                                return (FONDO_DER-10, SAQUE)
                            else:
                                return FONDO_DER-10, 340
                        else:
                            return FONDO_DER-10, 420
        else:
            # logica del jugador de campo
            # ESTRATEGIA: si mi equipo tiene la pelota avanzo, caso contrario retrocedo a marcar al rival
            # - si avanzo lo hago hacia los costados de mi rival, es decir, buscando el hueco libre
            # - si retrocedo el jugador de mi equipo mas cercano a la pelota va a presionar al rival que la tiene,
            # mientras que los otros marcan POR LA ESPALDA a los demas rivales
            '''
            # si tengo la pelota no me muevo porque voy la pase
            if player.hasBall:
                return player.rect.centerx, player.rect.centery
            else:
            '''
            # si mi equipo tiene la pelota avanzo hasta el area rival
            # los puntas si se encuentran en mitad de cancha rival se dirigen hacia el centro en diagonal y sino simplemente avanzan en x
            # los centrales avanzan solo en x
            if player.hasBall or self.isMyTeamWithBall(player.team): # el metodo ya chequea si la tiene el jugador, es por prueba el hasball
                if player.team:
                    if player.rect.centery > AREA_C_INF:
                        if player.rect.centerx < MITAD_CANCHA:
                            return player.rect.centerx+10, player.rect.centery
                        elif player.rect.centerx < AREA_G_MID_DER+10:
                            return player.rect.centerx+10, player.rect.centery-5
                        else:
                            return player.rect.centerx, player.rect.centery-10
                    elif player.rect.centery < AREA_C_SUP:
                        if player.rect.centerx < MITAD_CANCHA:
                            return player.rect.centerx+10, player.rect.centery
                        elif player.rect.centerx < AREA_G_MID_DER+10:
                            return player.rect.centerx+10, player.rect.centery+5
                        else:
                            return player.rect.centerx, player.rect.centery+10
                    elif player.rect.centerx < AREA_C_MID_DER:
                        return player.rect.centerx+10, player.rect.centery
                    else:
                        return player.rect.centerx-10, player.rect.centery
                else:
                    if player.rect.centery > AREA_C_INF:
                        if player.rect.centerx > MITAD_CANCHA:
                            return player.rect.centerx-10, player.rect.centery
                        elif player.rect.centerx > AREA_G_MID_IZQ-10:
                            return player.rect.centerx-10, player.rect.centery-5
                        else:
                            return player.rect.centerx, player.rect.centery-10
                    elif player.rect.centery < AREA_C_SUP:
                        if player.rect.centerx > MITAD_CANCHA:
                            return player.rect.centerx-10, player.rect.centery
                        elif player.rect.centerx > AREA_G_MID_IZQ-10:
                            return player.rect.centerx-10, player.rect.centery+5
                        else:
                            return player.rect.centerx, player.rect.centery+10
                    elif player.rect.centerx > AREA_C_MID_IZQ:
                        return player.rect.centerx-10, player.rect.centery
                    else:
                        return player.rect.centerx+10, player.rect.centery

            # si el equipo rival tiene la pelota 
            if self.isMyrivalTeamWithBall(player.team):
                
                # si estoy fuera del area grande y los rivales estan en su mitad de cancha retrocedo 
                if (player.team) and (ball_centerx > MITAD_CANCHA):
                        if player.rect.centerx > AREA_G_MID_IZQ:
                            return player.rect.centerx-10, player.rect.centery
                        return player.rect.centerx+10, player.rect.centery
                elif (not player.team) and (ball_centerx < MITAD_CANCHA):
                        if player.rect.centerx < AREA_G_MID_DER:
                            return player.rect.centerx+10, player.rect.centery
                        return player.rect.centerx-10, player.rect.centery
                
                # Chequear si algún compañero está más cerca de la pelota, sino voy yo a por ella (codigo repetido abajo)
                teammates = self.mediator.getTeammates(player.team)
                distance_to_teammate = 0
                min_distance_to_teammate = float('inf')
                for teammate in teammates:
                    if teammate != player:
                        distance_to_teammate = self.distance_to_ball(teammate, ball_centerx, ball_centery)
                        if distance_to_teammate < min_distance_to_teammate:
                            min_distance_to_teammate = distance_to_teammate
                # Si soy el jugador de mi equipo que se encuentra más cerca de la pelota voy hacia ella
                if min_distance_to_teammate > self.distance_to_ball(player, ball_centerx, ball_centery):
                    return ball_centerx, ball_centery

                # en la mitad de cancha de mi equipo marco al juagador de campo rival mas cercano que no este siendo marcado por un compañero
                teammates = self.mediator.getTeammates(player.team)
                rivals = self.mediator.getRivals(player.team)
                distance_to_rival = 0
                min_distance_to_rival = float('inf')
                # por defecto me quedo en mi posicion actual
                if player.team:
                    x, y = player.rect.centerx, player.rect.centery
                else:
                    x, y = player.rect.centerx, player.rect.centery

                for rival in rivals:
                    if not isinstance(rival, GoalKeeper):
                        distance_to_rival = self.distance_to_player(player, rival)
                        # Verificar si es el rival mas cercano y si eres el jugador más cercano entre tus compañeros a el
                        if distance_to_rival < min_distance_to_rival and all(self.distance_to_player(teammate, rival) > distance_to_rival for teammate in teammates if teammate != player):
                            x, y = rival.rect.centerx, rival.rect.centery
                            min_distance_to_rival = distance_to_rival
                return x, y
                            
            # si la pelota esta suelta (ningun jugador tiene posesión de ella)
            # Chequear si algún compañero está más cerca de la pelota, sino voy yo a por ella
            teammates = self.mediator.getTeammates(player.team)
            distance_to_teammate = 0
            min_distance_to_teammate = float('inf')
            for teammate in teammates:
                if teammate != player:
                    distance_to_teammate = self.distance_to_ball(teammate, ball_centerx, ball_centery)
                    if distance_to_teammate < min_distance_to_teammate:
                        min_distance_to_teammate = distance_to_teammate
            # Si soy el jugador de mi equipo que se encuentra más cerca de la pelota voy hacia ella
            if min_distance_to_teammate > self.distance_to_ball(player, ball_centerx, ball_centery):
                return ball_centerx, ball_centery
            
            # sino, mientras mi compañero va a buscar la pelota:      
            # si la pelota esta en mi area marco al rival mas cercano que no este siendo marcad por un compañero (codigo repetido) 
            if ((player.team) and (ball_centerx < MITAD_CANCHA)) or ((not player.team) and (ball_centerx > MITAD_CANCHA)):     
                teammates = self.mediator.getTeammates(player.team)
                rivals = self.mediator.getRivals(player.team)
                distance_to_rival = 0
                min_distance_to_rival = float('inf')
                # por defecto me quedo en mi posicion actual
                if player.team:
                    x, y = player.rect.centerx, player.rect.centery
                else:
                    x, y = player.rect.centerx, player.rect.centery

                for rival in rivals:
                    if not isinstance(rival, GoalKeeper):
                        distance_to_rival = self.distance_to_player(player, rival)
                        # Verificar si es el rival mas cercano y si eres el jugador más cercano entre tus compañeros a el
                        if distance_to_rival < min_distance_to_rival and all(self.distance_to_player(teammate, rival) > distance_to_rival for teammate in teammates if teammate != player):
                            x, y = rival.rect.centerx, rival.rect.centery
                            min_distance_to_rival = distance_to_rival
                return x, y
            '''
            # si la pelota esta en mi area marco al rival mas cercano (codigo repetido)
            if ((player.team) and (ball_centerx < MITAD_CANCHA)) or ((not player.team) and (ball_centerx > MITAD_CANCHA)):
                teammates = self.mediator.getTeammates(player.team)
                rivals = self.mediator.getRivals(player.team)
                min_distance_to_rival = float('inf')
                x, y = player.rect.centerx, player.rect.centery
                for rival in rivals:
                    distance_to_rival_squared = math.sqrt((rival.rect.centerx - player.rect.centerx)**2 + (rival.rect.centery - player.rect.centery)**2)
                    for teammate in teammates:
                        if teammate != player:
                            teammate_distance_to_rival_squared = math.sqrt((teammate.rect.centerx - rival.rect.centerx)**2 + (teammate.rect.centery - rival.rect.centery)**2)
                            if teammate_distance_to_rival_squared > distance_to_rival_squared and \
                            teammate_distance_to_rival_squared < min_distance_to_rival:
                                x, y = rival.rect.centerx, rival.rect.centery
                                min_distance_to_rival = teammate_distance_to_rival_squared

                return x, y
            '''
            # si la pelota esta en area rival, si estoy en area rival retrocedo y sino avanzo hasta el area grande rival
            if player.team:                
                if player.rect.centery > AREA_C_INF:
                    if player.rect.centerx < MITAD_CANCHA:
                        return player.rect.centerx+10, player.rect.centery
                    elif player.rect.centerx < AREA_G_MID_DER+10:
                        return player.rect.centerx+10, player.rect.centery-5
                    else:
                        return player.rect.centerx, player.rect.centery-10
                elif player.rect.centery < AREA_C_SUP:
                    if player.rect.centerx < MITAD_CANCHA:
                        return player.rect.centerx+10, player.rect.centery
                    elif player.rect.centerx < AREA_G_MID_DER+10:
                        return player.rect.centerx+10, player.rect.centery+5
                    else:
                        return player.rect.centerx, player.rect.centery+10
                elif player.rect.centerx < AREA_C_MID_DER:
                    return player.rect.centerx+10, player.rect.centery
                else:
                    return player.rect.centerx-10, player.rect.centery
            else:
                if player.rect.centery > AREA_C_INF:
                    if player.rect.centerx > MITAD_CANCHA:
                        return player.rect.centerx-10, player.rect.centery
                    elif player.rect.centerx > AREA_G_MID_IZQ-10:
                        return player.rect.centerx-10, player.rect.centery-5
                    else:
                        return player.rect.centerx, player.rect.centery-10
                elif player.rect.centery < AREA_C_SUP:
                    if player.rect.centerx > MITAD_CANCHA:
                        return player.rect.centerx-10, player.rect.centery
                    elif player.rect.centerx > AREA_G_MID_IZQ-10:
                        return player.rect.centerx-10, player.rect.centery+5
                    else:
                        return player.rect.centerx, player.rect.centery+10
                elif player.rect.centerx > AREA_C_MID_IZQ:
                    return player.rect.centerx-10, player.rect.centery
                else:
                    return player.rect.centerx+10, player.rect.centery

            '''
                # marco al rival mas cercano que tengo no marcado por un compañero
                teammates = self.mediator.getTeammates(player.team)
                rivals = self.mediator.getRivals(player.team)
                min_distance_to_rival = float('inf')
                distance_to_rival_squared = 0
                teammte_distance_to_rival_squared = 0
                x, y = player.rect.centerx, player.rect.centery
                for rival in rivals:
                    distance_to_rival_squared = math.sqrt((rival.rect.centerx - player.rect.centerx)**2 + (rival.rect.centery - player.rect.centery)**2)
                    for teammate in teammates:
                        if teammate != player:
                            teammte_distance_to_rival_squared = math.sqrt((teammate.rect.centerx - rival.rect.centerx)**2 + (teammate.rect.centery - rival.rect.centery)**2)
                            # Si estoy más cerca del rival que mi compañero, lo marco
                            if teammte_distance_to_rival_squared > distance_to_rival_squared and \
                            teammte_distance_to_rival_squared > min_distance_to_rival:
                                x, y = rival.rect.centerx, rival.rect.centery
                                print("QUE ONDA")
                                min_distance_to_rival = teammte_distance_to_rival_squared
                return x, y
                '''
            '''
                teammates = self.mediator.getTeammates(player.team)
                rivals = self.mediator.getRivals(player.team) 
                min_distance_to_rival = 10000000
                distance_to_rival = 0
                teammte_distance_to_rival = 0
                x = player.rect.centerx
                y = player.rect.centery
                for rival in rivals:
                    distance_to_rival = math.sqrt((rival.rect.centerx - player.rect.centerx)**2 + (rival.rect.centery - player.rect.centery)**2)
                    if distance_to_rival < min_distance_to_rival:
                        min_distance_to_rival = distance_to_rival
                    for teammate in teammates:
                        if teammate != player:
                            teammte_distance_to_rival = math.sqrt((rival.rect.centerx - teammate.rect.centerx)**2 + (rival.rect.centery - teammate.rect.centery)**2)
                            # si estoy mas cerca del rival que mi compañero yo lo marco (el mas cercano que encuentre)
                            if teammte_distance_to_rival > distance_to_rival and teammte_distance_to_rival > min_distance_to_rival:                              
                                x = rival.rect.centerx
                                y = rival.rect.centery
                return x, y
                '''

    def with_ball(self, player):
        # 1 -> patear | 2 -> pasar | 3 -> moverse
        if isinstance(player, GoalKeeper):
            return 2
        else:
            # si estoy en el area grande rival pateo
            if player.team:
                if (player.rect.centerx > AREA_G_MID_DER) and (AREA_C_SUP < player.rect.centery < AREA_C_INF):
                    return 1
            else:
                if (player.rect.centerx < AREA_G_MID_IZQ) and (AREA_C_SUP < player.rect.centery < AREA_C_INF):
                    return 1
            # si no puedo patear chequeo si tengo marca (la paso, sino me muevo hacia el area rival)
            if self.marked_player(player):
                return 2
            return 3

    '''        
    def calcular_distancia_cuadrada(self, punto1, punto2):
        return (punto2[0] - punto1[0])**2 + (punto2[1] - punto1[1])**2

    def find_the_furthest_player(self, player, teammates, rivals):
        max_distance_general = -1
        jugador_mas_alejado = None

        for teammate in teammates:
            if teammate != player:
                distancia_minima_rival = min(self.calcular_distancia_cuadrada(teammate.rect.center, rival.rect.center) for rival in rivals)
                if distancia_minima_rival > max_distance_general:
                    max_distance_general = distancia_minima_rival
                    jugador_mas_alejado = teammate

        return jugador_mas_alejado.rect.center if jugador_mas_alejado else (MITAD_CANCHA, SAQUE)
    '''
    
    def find_the_furthest_player(self, player, teammates, rivals):
        max_distance_general = -1
        teammate_distance_to_rival = 0
        # despeje hacia abajo en caso de que todos los compañeros esten a la espalda de su marca para evitar pasarsela al rival
        x, y = player.rect.centerx, LATERAL_DER
        for rival in rivals:
            for teammate in teammates:
                if teammate != player:
                    # verificar que el jugador no este a la espalda del rival para evitar pases al rival
                    if (player.team and teammate.rect.centerx < rival.rect.centerx) or \
                    (not player.team and teammate.rect.centerx > rival.rect.centerx):
                        
                        teammate_distance_to_rival = self.distance_to_player(teammate, rival)
                        if teammate_distance_to_rival > max_distance_general:
                            max_distance_general = teammate_distance_to_rival
                            x, y = teammate.rect.centerx, teammate.rect.centery
        return x, y

    def where_to_pass(self, player):
        teammates = self.mediator.getTeammates(player.team)
        # si tengo la pelota en mi mitad de cancha se la paso al compañero que tenga la marca mas alejada
        if (player.team and player.rect.centerx <= MITAD_CANCHA) or (not player.team and player.rect.centerx >= MITAD_CANCHA):
            rivals = self.mediator.getRivals(player.team)
            return self.find_the_furthest_player(player, teammates, rivals)
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