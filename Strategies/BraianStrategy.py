from Strategies.Strategy import Strategy
import random
from Constantes import *
from players.GoalKeeper import GoalKeeper
import math

class BraianStrategy(Strategy):
    DISTANCIA_DE_MARCADO = 80


    def _init_(self):
        super()._init_()
    
    #equipo1 va a la izq
    #player.team = true izq
    def jugarSinPelota(self,player):
        aux = player.mediator.getTeammates(player.team)
        #pregunto que equipo es true es la izq
        if (player.team):
            #recorro el equipo
            for i in aux:
                if (i != player) and not isinstance(i,GoalKeeper):
                    # si mi companiero esta mas a la derecha que yo, estoy habilitado para quedarme
                    if (i.rect.centerx < player.rect.centerx):
                        #IMPORTANTE chequear limites cuando le pido que haga +10 ver hasta donde avanza
                        if (player.rect.centerx+10 < AREA_G_MID_DER):
                            return player.rect.centerx+10, player.rect.centery
                        else:
                            return player.rect.centerx-5, player.rect.centery
            return player.rect.centerx, player.rect.centery
        # si es del otro equipo        
        else:
            for i in aux:
                if (i != player):
                    # si mi companiero esta mas a la izquierda que yo, estoy habilitado para quedarme
                    if (i.rect.centerx > player.rect.centerx):
                        #IMPORTANTE chequear limites cuando le pido que haga -10 ver hasta donde avanza
                        if (player.rect.centerx-10 > AREA_G_MID_IZQ):
                            return player.rect.centerx-10, player.rect.centery
                        else:
                            return player.rect.centerx+5, player.rect.centery
            return player.rect.centerx, player.rect.centery

    def tenemosPelota(self, player):
        aux = player.mediator.getTeammates(player.team)
        hayPosesion=False
        for i in aux:
            if (i.hasBall) and (i!= player):
                hayPosesion=True
                return hayPosesion
        return hayPosesion

    def rivalLejos(self,rival,player):
        if ((rival.rect.centerx - player.rect.centerx >= 50 or rival.rect.centerx - player.rect.centerx >= -50) and (rival.rect.centery - player.rect.centery >= 50 or rival.rect.centery - player.rect.centery >= -50)):
            return None
        else:
            return rival

    def soyMasCercano(self,player):
        aux = player.mediator.getTeammates(player.team)
        
        for i in aux:
            pelota_x, pelota_y = player.mediator.getBallsPosition()
            if self.calculo_de_distancia(i.rect.centerx,i.rect.centery,pelota_x,pelota_y) < \
                (self.calculo_de_distancia(player.rect.centerx,player.rect.centery,pelota_x,pelota_y)):
                return False       
        return True


    ##########################################a#####################################

    def MiequipoTienePelota(self,player):
        myTeam = player.mediator.getTeammates(player.team)
        for teammate in myTeam:
                if teammate.hasBall:
                    return True
        return False
    
    def RivalTienePelota(self,player):
        rivals = player.mediator.getRivals(player.team)
        for rival in rivals:
                if rival.hasBall:
                    return True
        return False
    
    def distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

    def distance_to_player(self, player1, player2):
        return self.distance((player1.rect.centerx, player1.rect.centery), (player2.rect.centerx, player2.rect.centery))


    def esMasCercano(self, player):
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
        if self.esMasCercano(player):
            return px, py
        else: 
            # Verificar si el rival más cercano no está siendo marcado
            closest_unmarked_rival = min(rivals, key=lambda r: self.distance_to_player(r, player))
            if not self.esta_marcado(closest_unmarked_rival):
                return self.mano_a_mano(player, closest_unmarked_rival)
            # Vuelvo en X tanto como lo haga la pelota, considerando el equipo
            if player.team:
                return x - (px - x), y  # Retroceder hacia la izquierda
            else:
                return x + (px - x), y  # Retroceder hacia la derecha

    def esta_marcado(self, rival):
        teammates= rival.mediator.getRivals(rival.team)
        for teammate in teammates:
            distance= self.distance_to_player(rival,teammate)
            if distance< 40:
                return True
        return False

    def mano_a_mano(self, player, rival):
        # Calcular la distancia al rival objetivo
        distance_to_rival = self.distance_to_player(player, rival)
        #umbral para la marca personal
        marking_threshold = 50
        # Verificar si la distancia al rival está dentro del umbral para activar la marca personal
        if distance_to_rival <= marking_threshold:
            # Moverse hacia la posición del rival objetivo
            return rival.rect.centerx, rival.rect.centery
        return player.rect.centerx, player.rect.centery
    
    def movimiento_jugador_con_pelota(self, player):
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

    def mover_arquero(self, goalkeeper):
        # Definir un atributo booleano en el arquero
        if not hasattr(goalkeeper, 'moving_up'):
            goalkeeper.moving_up = True
        px, py = goalkeeper.mediator.getBallsPosition()
        # Distancia mínima para activar el movimiento hacia la pelota en el eje Y
        R = 150
        # Calcular la distancia entre el arquero y la pelota
        distancia_pelota = math.hypot(goalkeeper.rect.centerx - px, goalkeeper.rect.centery - py)
        # Verificar si la pelota está a una distancia menor o igual a R
        if self.esMasCercano(goalkeeper)and distancia_pelota<=250:
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
            return self.mover_arquero(player)
        else:
            #si mi equipo tiene la pelota
            MiequipoTienePelota = self.MiequipoTienePelota(player)
            if player.hasBall or MiequipoTienePelota:
                x,y= self.movimiento_jugador_con_pelota(player)
                return x,y
            #si el rival tiene la pelota
            if self.RivalTienePelota(player):
                return self.player_movement_rival_with_ball(player)
            #si la pelota esta suelta
            if self.esMasCercano(player):
                return px,py
        return player.rect.centerx + random.uniform(-10,10),player.rect.centery + random.uniform(-5,5) 

    ##########################################a#####################################   
    # Función para calcular la distancia entre dos puntos
    def calculo_de_distancia(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    # Retorna si el player esta marcado.
    def jugadorMarcado(self, player):
        rivals = self.mediator.getRivals(player.team)
        for rival in rivals:
            # La marca sera sobre el eje x
            if ((player.team) and (player.rect.centerx < rival.rect.centerx)) or ((not player.team) and (player.rect.centerx > rival.rect.centerx)):
                    #Chequeamos si la distancia entre los jugadores es menor a lo que nosotros consideramos que un jugador esta marcado por otro
                    if self.calculo_de_distancia(player.rect.centerx, rival.rect.centerx, player.rect.centery, rival.rect.centery) < self.DISTANCIA_DE_MARCADO:
                        return True
        return False
    
    #Que vas a hacer cuando tengas la pelota
    def with_ball(self, player):
        if isinstance(player, GoalKeeper):
            return 2    #Recordar que no tengo que devolver una coordenada, solamente un return1,2,3
        else:
            # Si el jugador se encuentra en el area del equipo rival intentaremos que patee
            if player.team:
                if (player.rect.centerx > AREA_G_MID_DER) and (AREA_C_SUP < player.rect.centery < AREA_C_INF):
                    return 1
            else:
                if (player.rect.centerx < AREA_G_MID_IZQ) and (AREA_C_SUP < player.rect.centery < AREA_C_INF):
                    return 1
            # si no puedo patear chequeo si tengo marca (la paso, sino me muevo hacia el area rival)
            if self.jugadorMarcado(player):
                return 2
            return 3

    
    
    def distancia_entre_puntos(self, punto1, punto2):
        return math.sqrt((punto2[0] - punto1[0]) ** 2 + (punto2[1] - punto1[1]) ** 2)


    def pasar_mas_cercano(self, player):
        companieros = player.mediator.getTeammates(player.team)
            
        # Inicializar con un valor grande para comparar
        distancia_minima = float('inf')
        companero_mas_cercano = None

        for companiero in companieros:
            if (companiero != player):
                # Obtener las coordenadas del centro del jugador y del compañero
                centro_jugador = (player.rect.centerx, player.rect.centery)
                centro_companiero = (companiero.rect.centerx, companiero.rect.centery)

                # Calcular la distancia entre el jugador y el compañero
                distancia_actual = self.distancia_entre_puntos(centro_jugador, centro_companiero)

                # Verificar si la distancia actual es menor que la mínima encontrada hasta ahora
                if distancia_actual < distancia_minima:
                    distancia_minima = distancia_actual
                    companero_mas_cercano = centro_companiero

        return companero_mas_cercano

    #Elegir a que companiero se la quiero pasar
    def where_to_pass(self, player):
        #No chequeo si es arquero o no porque quiero pasarla al mas cercano
        result = self.pasar_mas_cercano(player)
        return result