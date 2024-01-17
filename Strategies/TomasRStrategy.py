from Strategies.Strategy import Strategy
import math
from Constantes import *
from players.GoalKeeper import GoalKeeper

class TomasRStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def isMyTeamWithBall(self, player):
        teammates = self.mediator.getTeammates(player.team)
        for teammate in teammates:
            if teammate.hasBall:
                return True
        return False

    def getProxPos(self, player):
        # return player.rect.centerx, player.rect.centery
        ball_centerx, ball_centery = self.mediator.getBallsPosition()
        if isinstance(player, GoalKeeper):
            if player.hasBall:
                # moverme hacia abajo o hacia arriba para llevarme la marca y pasarsela al que se desmarque
                # (si me muevo hacia arriba el de abajo se desmarca y si me muevo hacia abajo el de arriba se desmarca)
                if player.team:
                    if player.rect.centery < SAQUE:
                        return FONDO_IZQ+10, PALO_INF
                    return FONDO_IZQ+10, PALO_SUP
                else:
                    if player.rect.centery < SAQUE:
                        return FONDO_DER-10, PALO_INF
                    return FONDO_DER-10, PALO_SUP
            else:
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
                if self.isMyTeamWithBall(player):
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
                                    print ("A")
                                    return (FONDO_IZQ+10, SAQUE)
                                else:
                                    print("B")
                                    return FONDO_IZQ+10, 340
                            else:
                                print("C")
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
            if player.hasBall:
                # que no se mueva, que la pase
                print("TTT")
                return player.rect.centerx, player.rect.centery
            else:
                if self.isMyTeamWithBall(player):
                    if player.team:
                        return player.rect.centerx+10, player.rect.centery
                    else:
                        return player.rect.centerx-10, player.rect.centery
                else:
                    #if ball_centerx < MITAD_CANCHA:
                    # marco al rival mas cercano que tengo no marcado por un compañero
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
                                teammte_distance_to_rival = math.sqrt((teammate.rect.centerx - rival.rect.centerx)**2 + (teammate.rect.centery - rival.rect.centery)**2)
                                # si estoy mas cerca del rival que mi compañero yo lo marco (el mas cercano que encuentre)
                                if teammte_distance_to_rival > distance_to_rival and teammte_distance_to_rival > min_distance_to_rival:                              
                                    x = rival.rect.centerx
                                    y = rival.rect.centery
                    return x, y
                    #else:

    def with_ball(self, player):
        # 1 -> patear | 2 -> pasar | 3 -> moverse
        return 2
        if isinstance(player, GoalKeeper):
            # si el arquero esta en el area grande la pasa al recibir la pelota, sino se mueve para eludir rivales
            # y abrir la marca
            if player.team:
                if player.rect.centerx > AREA_C_MID_IZQ:
                    return 2
                else:
                    return 3
            else:
                if player.rect.centerx < AREA_C_MID_DER:
                    return 2
                else:
                    return 3
        else:
            # si no puedo patear al arco la paso, no me muevo con la pelota, me conviene pasarla, jugar a primer toque
            # 27 px de width y height el sprite del player
            if player.team:
                # si estoy en el area grande rival y no tengo ningun rival enfrente pateo, sino la paso
                # if player.rect.centerx > AREA_C_MID_IZQ:
                if player.rect.centerx > AREA_C_MID_DER:
                    rivals = self.mediator.getRivals(player.team)
                    for rival in rivals:
                        if rival.rect.centerx > player.rect.centerx:
                            if player.rect.centery-40 < rival.rect.centery < player.rect.centery+40:
                                # rival frente a mi -> la paso
                                return 2
                    return 1
                return 2
            else:
                # si estoy en el area grande rival y no tengo ningun rival enfrente pateo, sino la paso
                #if player.rect.centerx < AREA_C_MID_DER:
                if player.rect.centerx < AREA_C_MID_IZQ:
                    rivals = self.mediator.getRivals(player.team)
                    for rival in rivals:
                        if rival.rect.centerx < player.rect.centerx:
                            if player.rect.centery-40 < rival.rect.centery < player.rect.centery+40:
                                # rival frente a mi -> la paso
                                return 2
                    return 1
                return 2
            
    def calcular_distancia_cuadrada(self, punto1, punto2):
        return (punto2[0] - punto1[0])**2 + (punto2[1] - punto1[1])**2

    def encontrar_jugador_mas_alejado(self, player, teammates, rivals):
        max_distance_general = -1
        jugador_mas_alejado = None

        for teammate in teammates:
            if teammate != player:
                distancia_minima_rival = min(self.calcular_distancia_cuadrada(teammate.rect.center, rival.rect.center) for rival in rivals)
                if distancia_minima_rival > max_distance_general:
                    max_distance_general = distancia_minima_rival
                    jugador_mas_alejado = teammate

        return jugador_mas_alejado.rect.center if jugador_mas_alejado else (MITAD_CANCHA, SAQUE)

    def where_to_pass(self, player):
        return MITAD_CANCHA-200, AREA_G_INF+50
        '''
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)

        return self.encontrar_jugador_mas_alejado(player, teammates, rivals)
        '''
'''
    def where_to_pass(self, player):
        # puedo:
        # pasarsela al jugador que este mas solo (es lo que tengo implementado)
        # pasarsela al compañero mas cercano
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)
        distance = 0
        max_distance = -1
        max_distance_general = -1
        x = MITAD_CANCHA
        y = SAQUE
        for teammate in teammates:
            if teammate != player:
                for rival in rivals:
                    distance = math.sqrt((rival.rect.centerx - teammate.rect.centerx)**2 + (rival.rect.centery - teammate.rect.centery)**2)
                    if distance > max_distance:
                        max_distance = distance
                if max_distance > max_distance_general:
                    max_distance_general = max_distance
                    x = teammate.rect.centerx
                    y = teammate.rect.centery
        return x, y
'''     

