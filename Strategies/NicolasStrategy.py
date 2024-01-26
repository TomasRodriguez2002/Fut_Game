from Strategies.strategy import Strategy
import random
from players.goalKeeper import GoalKeeper
from constantes import *

class NicolasStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.rivals=None
        self.teammates= None
        self.accion_movimiento=0
        self.cant_players_yendo_balon=0 #Valor entero que determina que postura tendra el jugador a moverse si el mismo posee el balon (0->Sigo normalmente, 1->esquivo a los rivales, 2-> me voy hacia los alterales)
        self.distanciaMaxPase=200
        self.distanciaSegura=50
    #Obtener proxima posicion del q vas a pasar
    def getProxPos(self, player):
        self.teammates= self.mediator.getTeammates(player.team)
        self.rivals=self.mediator.getRivals(player.team)
        
        position_in_field = self.playerPositionInField(player) #CON POSITION EN FIELD ANTES DE RETORNAR LA POSICION NUEVA CHEQUEAR CON METODO SI ES POSIBLE O NO
        ball_position_in_field=self.playerPositionInField(self.mediator.ball)
        pos_ball_x,pos_ball_y = self.mediator.getBallsPosition()

        team_have_ball=self.teamHaveBall(self.teammates)
        rivals_have_ball=self.teamHaveBall(self.rivals)
        #Acciones si soy arquero
        if(isinstance(player,GoalKeeper)):
            if(team_have_ball):#Si mi eequipo posee el balon
                if(player.team):
                    next_pos_x=144
                    next_pos_y=383
                    return next_pos_x,next_pos_y #Me paro en el centro del arco esperando
                else:
                    next_pos_x=1200
                    next_pos_y=383
                    return next_pos_x,next_pos_y
            else:#Si mi equipo no posee el balon
                #-------------------------------LOGICA PARA ARQUERO EQUIPO 1---------------------------------
                if(player.team and pos_ball_x<=AREA_G_MID_IZQ and pos_ball_y>=AREA_G_SUP and pos_ball_y<=AREA_G_INF):#Si la pelota se encuentra en el area grande
                    if(pos_ball_x<=AREA_C_MID_IZQ):#si se encuentra la pelota en el area chica
                        if(team_have_ball):
                            next_pos_x=126
                            next_pos_y=pos_ball_y#Voy siguiendo a la pelota en eje y
                            return next_pos_x,next_pos_y
                        else:#Si mi equipo no tiene la pelota no me queda otra q ir a buscarla para achicar distancia
                            next_pos_x=pos_ball_x
                            next_pos_y=pos_ball_y
                            return next_pos_x,next_pos_y
                    if(not self.nearbyAlliesAtRange(player)):#Si no hay compañeros cerca
                        next_pos_x=pos_ball_x
                        next_pos_y=pos_ball_y
                        return next_pos_x,next_pos_y
                    elif(pos_ball_y<=PALO_SUP):#Si la pelota se encuentra por arriba del palo
                        next_pos_x=126
                        next_pos_y=317
                        return next_pos_x,next_pos_y#Me paro como arquero en el borde del palo superior
                    elif(pos_ball_y>=PALO_INF):#Si la pelota se encuentra por debajo del palo inferior
                        next_pos_x=126
                        next_pos_y=447
                        return next_pos_x,next_pos_y#Me paro como arquero en el borde del palo inferior
                    else:#Si la pelota se encuentra dentro del area grande pero en una altura similar a los palos
                        next_pos_x=126
                        next_pos_y=pos_ball_y#Voy siguiendo a la pelota en eje y
                        return next_pos_x,next_pos_y
                elif(player.team and pos_ball_x>AREA_G_MID_IZQ):#Si se encuentra la pelota en cualquier parte de la cancha que no sea el area
                    next_pos_x=144
                    next_pos_y=383
                    return next_pos_x,next_pos_y #Me quedo esperando en el medio del arco
                
                #-------------------------------LOGICA PARA ARQUERO EQUIPO 2---------------------------------
                if(not player.team and pos_ball_x>=AREA_G_MID_DER):#Si la pelota se encuentra en el area grande
                    if(pos_ball_x>=AREA_C_MID_DER):#si se encuentra la pelota en el area chica
                        if(team_have_ball):
                            next_pos_x=1224
                            next_pos_y=pos_ball_y#Voy siguiendo a la pelota en eje y
                            return next_pos_x,next_pos_y
                        else:#Si mi equipo no tiene la pelota no me queda otra q ir a buscarla para achicar distancia
                            next_pos_x=pos_ball_x
                            next_pos_y=pos_ball_y
                            return next_pos_x,next_pos_y
                    
                    if(not self.nearbyAlliesAtRange(player)):#Si no hay compañeros cerca
                        next_pos_x=pos_ball_x
                        next_pos_y=pos_ball_y
                        return next_pos_x,next_pos_y
                    elif(pos_ball_y<=PALO_SUP):#Si la pelota se encuentra por arriba del palo
                        next_pos_x=1224
                        next_pos_y=317
                        return next_pos_x,next_pos_y#Me paro como arquero en el borde del palo superior
                    elif(pos_ball_y>=PALO_INF):#Si la pelota se encuentra por debajo del palo inferior
                        next_pos_x=1224
                        next_pos_y=447
                        return next_pos_x,next_pos_y#Me paro como arquero en el borde del palo inferior
                    else:#Si la pelota se encuentra dentro del area grande pero en una altura similar a los palos
                        next_pos_x=1224
                        next_pos_y=pos_ball_y#Voy siguiendo a la pelota en eje y
                        return next_pos_x,next_pos_y

    
                elif(not player.team and pos_ball_x<AREA_G_MID_DER):#Si se encuentra la pelota en cualquier parte de la cancha que no sea el area
                    next_pos_x=1200
                    next_pos_y=383
                    return next_pos_x,next_pos_y #Me quedo esperando en el medio del arco

        #--------------------------LOGICA PARA JUGADORES------------------
        if(team_have_ball):#Si mi equipo tiene la pelota
            if(player.hasBall):#Si yo tengo el balon
                if(self.accion_movimiento==0):#Si al tener el balon tengo q seguir recto hacia el arco
                    if(player.team):
                        next_pos_x=player.rect.centerx+10
                        next_pos_y=player.rect.centery
                        return next_pos_x,next_pos_y
                    else:
                        next_pos_x=player.rect.centerx-10
                        next_pos_y=player.rect.centery
                        return next_pos_x,next_pos_y
                elif(self.accion_movimiento==1):#Si al tener el balon tengo que esquivar a los jugadores cercanos
                    closest_rival=self.nearestEnemy(player)#Obtengo al jugador mas cercano
                    if(player.team):#Logica player equipo 1
                        if(closest_rival.rect.centery<=player.rect.centery):#Si el player enemigo se encuentra encima mio
                            next_pos_x=player.rect.centerx+10
                            next_pos_y=player.rect.centery+5
                            return next_pos_x,next_pos_y
                        elif(closest_rival.rect.centery>=player.rect.centery):#Si el player enemigo se encuentra debajo mio
                            next_pos_x=player.rect.centerx+10
                            next_pos_y=player.rect.centery-5
                            return next_pos_x,next_pos_y
                        elif(closest_rival.rect.centerx>player.rect.centery and -3<=(closest_rival.rect.centery-player.rect.centery)<=3):#Si el player enemigo se encuentra a mi derecha
                            next_pos_x=player.rect.centerx-2#PROBAR SI ES MEJOR ADELANTAR ENDEVES DE IRSE PARA ATRAS
                            if(random.choice([True,False])):
                                next_pos_y=player.rect.centery+10
                            else:
                                next_pos_y=player.rect.centery-10
                            return next_pos_x,next_pos_y
                        elif(closest_rival.rect.centerx<player.rect.centery and -3<=(closest_rival.rect.centery-player.rect.centery)<=3):#Si el player enemigo se encuentra a mi izquierda
                            next_pos_x=player.rect.centerx+20
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                    else:#Logica player equipo 2
                        if(closest_rival.rect.centery<player.rect.centery):#Si el player enemigo se encuentra encima mio
                            next_pos_x=player.rect.centerx-10
                            next_pos_y=player.rect.centery+5
                            return next_pos_x,next_pos_y
                        elif(closest_rival.rect.centery>player.rect.centery):#Si el player enemigo se encuentra debajo mio
                            next_pos_x=player.rect.centerx-10
                            next_pos_y=player.rect.centery-5
                            return next_pos_x,next_pos_y
                        elif(closest_rival.rect.centerx>player.rect.centery and -3<=(closest_rival.rect.centery-player.rect.centery)<=3):#Si el player enemigo se encuentra a mi derecha
                            next_pos_x=player.rect.centerx+2#PROBAR SI ES MEJOR ADELANTAR ENDEVES DE IRSE PARA ATRAS
                            if(random.choice([True,False])):
                                next_pos_y=player.rect.centery+10
                            else:
                                next_pos_y=player.rect.centery-10
                            return next_pos_x,next_pos_y
                        elif(closest_rival.rect.centerx<player.rect.centery and -3<=(closest_rival.rect.centery-player.rect.centery)<=3):#Si el player enemigo se encuentra a mi izquierda
                            next_pos_x=player.rect.centerx-20
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                        
                else:#Si al tener el balon tengo que irme hacia los laterales
                    if(player.team):
                        if(player.rect.centery>=SAQUE):#Si me encuentro por debajo de la mitad de la cancha
                            next_pos_x=player.rect.centerx+2
                            next_pos_y=player.rect.centery+5
                            if(next_pos_y>LATERAL_DER):
                                return next_pos_x,next_pos_y
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                        else:
                            next_pos_x=player.rect.centerx+5
                            next_pos_y=player.rect.centery-10
                            if(next_pos_y<LATERAL_IZQ):
                                return next_pos_x,next_pos_y
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                    else:
                        if(player.rect.centery>=SAQUE):#Si me encuentro por debajo de la mitad de la cancha
                            next_pos_x=player.rect.centerx-5
                            next_pos_y=player.rect.centery+10
                            if(next_pos_y>LATERAL_DER):
                                return next_pos_x,next_pos_y
                            return next_pos_x,next_pos_y
                        else:
                            next_pos_x=player.rect.centerx-5
                            next_pos_y=player.rect.centery-10
                            if(next_pos_y<LATERAL_IZQ):
                                return next_pos_x,next_pos_y
                            return next_pos_x,next_pos_y
           
            else:#Si yo no soy el jugador que posee el balon
                if(player.team):
                    if(position_in_field==2):
                        next_pos_x=player.rect.centerx+ random.randint(-1,1)
                        next_pos_y=player.rect.centery + random.randint(-1,1)
                        return next_pos_x,next_pos_y
                    else:
                        next_pos_x=player.rect.centerx+3
                        next_pos_y=player.rect.centery
                        return next_pos_x,next_pos_y
                else:
                    if(position_in_field==4):
                        next_pos_x=player.rect.centerx+ random.randint(-1,1)
                        next_pos_y=player.rect.centery + random.randint(-1,1)
                        return next_pos_x,next_pos_y
                    else:
                        next_pos_x=player.rect.centerx-3
                        next_pos_y=player.rect.centery
                        return next_pos_x,next_pos_y
        else:#Si los rivales o ninguno de los dos equipos posee el balon
            if(self.closestTeammateToBall(player) or self.distancePlayerToObject(player,self.mediator.ball)<90): #Si soy el jugador mas cercano a la pelota o esta muy cerca mia
                next_pos_x=pos_ball_x
                next_pos_y=pos_ball_y
                return next_pos_x,next_pos_y#Voy hacia la pelota
            else:
                if(player.team):
                    if(rivals_have_ball or ball_position_in_field==1 or ball_position_in_field==4):#Si la pelota se encuentra en una zona critica para mi
                        if(position_in_field==4):#Si estoy en  el area me quedo en el area
                            next_pos_x=player.rect.centerx+ random.randint(-1,1)
                            next_pos_y=player.rect.centery + random.randint(-1,1)
                            return next_pos_x,next_pos_y
                        else:
                            next_pos_x=player.rect.centerx-3#Tengo q retroceder
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                    else:
                        if(position_in_field==2):#Si estoy en el area del enemigo
                            next_pos_x=player.rect.centerx+ random.randint(-1,1)
                            next_pos_y=player.rect.centery + random.randint(-1,1)
                            return next_pos_x,next_pos_y
                        else:
                            next_pos_x=player.rect.centerx+3#Sino avanzo
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                else:#Logica equipo 2
                    if(rivals_have_ball or ball_position_in_field==2 or ball_position_in_field==3):#Si la pelota se encuentra en una zona critica para mi
                        if(position_in_field==2):#Me quedo esperando en el area
                            next_pos_x=player.rect.centerx+ random.randint(-1,1)
                            next_pos_y=player.rect.centery + random.randint(-1,1)
                            return next_pos_x,next_pos_y
                        else:
                            next_pos_x=player.rect.centerx+3
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
                    else:
                        if(position_in_field==4):
                            next_pos_x=player.rect.centerx+ random.randint(-1,1)
                            next_pos_y=player.rect.centery + random.randint(-1,1)
                            return next_pos_x,next_pos_y
                        else:
                            next_pos_x=player.rect.centerx-3
                            next_pos_y=player.rect.centery
                            return next_pos_x,next_pos_y
        



        next_pos_x=random.randint(-10,10)+player.rect.centerx
        next_pos_y=random.randint(-10,10)+player.rect.centery
        return next_pos_x,next_pos_y
    def with_ball(self, player):#Devuelve numero que dice que estrategia hacer cuando el jugador posee el valon
        self.rivals=self.mediator.getRivals(player.team)
        self.teammates= self.mediator.getTeammates(player.team)
        position_in_field = self.playerPositionInField(player)  #Variable que guarda la ubicacion del jugador dentro de la cancha (0->)
        nearbyAllies = self.nearbyAlliesAtRange(player)
        nearbyEnemies = self.nearbyEnemies(player)
        #Si el jugador esta en una zona critica para patear al arco
        if (isinstance(player,GoalKeeper)):
            if(self.getQuantityOfNearbyEnemiesPlayers(player)>1):#Si hay mas de 1 player enemigo cerca mio
                return 1 #Mando la pelota al centro
            if(nearbyAllies):#Si es un arquero con la pelota y hay aliados cerca se las paso
                return 2
            else:#Si es un arquero y no hay aliados cerca la reviento a la mitad de la cancha
                return 1

        if(position_in_field==2 and player.team) or (position_in_field==4 and not player.team):
            if(nearbyEnemies):
                cant_nearby_enemies=self.getQuantityOfNearbyEnemiesPlayers(player)
                if(cant_nearby_enemies>2):#Si hay mas de 2 jugadores cubriendo al jugador hago pase
                    return 2
                else:#Sino pateo al arco
                    return 1
            else:
                return 1
        #Si el jugador esta en su area
        if(position_in_field==4 and player.team) or (position_in_field==2 and not player.team):
            if (not nearbyEnemies):#Si no hay jugadores enemigos cerca
                self.accion_movimiento=0
                return 3
            else:
                if(nearbyAllies):#Si hay jugadores amigos cerca
                    return 2
                else:#Hay jugadores enemigos cerca y no hay aliados a quien pasarsela
                    self.accion_movimiento=1 #Esquiva lo que puedas
                    return 3
                    
        if(position_in_field==1  or position_in_field==3):#Si el jugador se encuentra a la mitad de la cancha
            if(nearbyEnemies):#Si hay enemigos cerca
                if(self.getQuantityOfNearbyEnemiesPlayers(player)>1):#Hay mas de 1 solo enemigo cerca
                    self.accion_movimiento=1#Esquiva a ese jugador
                    return 3
                else:
                    if(nearbyAllies):#Si hay aliados cerca les paso la pelota
                        return 2
                    else:
                        self.accion_movimiento=2#Ve hacia los laterales
                        return 3
            else:
                self.accion_movimiento=0#movete en lina recta hacia el arco
                return 3
        
        if(position_in_field==1  or position_in_field==3):#Si el jugador se encuentra en los laterales
            if(nearbyEnemies):
                if(nearbyAllies):
                    return 2
                else:
                    self.accion_movimiento=1
                    return 3
            else:
                self.accion_movimiento=0
                return 3


    def where_to_pass(self, player):#Calcula hacia quien le debes dar el pase
        teammate_pos_x,teammate_pos_y=self.getTeammateForPass(player)
        return teammate_pos_x,teammate_pos_y



    #Saber si un equipo tiene el balon
    def teamHaveBall(self,teamWithPlayers):
        for jugador in teamWithPlayers:
            if(jugador.hasBall):
                return True
        return False
    def closestTeammateToBall(self,player):
        distance_to_ball=self.distancePlayerToObject(player,self.mediator.ball)
        for teammate in self.teammates:
            if(self.distancePlayerToObject(teammate,self.mediator.ball)<distance_to_ball):
                return False
        return True


    def distancePlayerToObject(self,player,objeto):
        dis_x_to_obj = objeto.rect.centerx-player.rect.centerx
        dis_pos_y_to_obj = objeto.rect.centery-player.rect.centery
        distance = (dis_x_to_obj ** 2 + dis_pos_y_to_obj** 2) ** 0.5
        return distance
    def getTeammateForPass(self,player):
        playerToPass=None
        quantityOfNearbyEnemiesMin=10
        for teammate in self.teammates:
            if(player.rect.centerx!=teammate.rect.centerx or player.rect.centery!=teammate.rect.centery):#Si no estoy hablando del mismo jugador
                nearbyEnemiesForThatTeammate=self.getQuantityOfNearbyEnemiesPlayers(teammate)
                if(nearbyEnemiesForThatTeammate<quantityOfNearbyEnemiesMin):
                    quantityOfNearbyEnemiesMin=nearbyEnemiesForThatTeammate
                    playerToPass=teammate
            
        return playerToPass.rect.centerx,playerToPass.rect.centery
    def nearbyAlliesAtRange(self,player):
        for teammate in self.teammates:
            if(self.distancePlayerToObject(player,teammate)< self.distanciaMaxPase):
                return True
        return False
    def nearbyEnemies(self,player):
        for rival in self.rivals:
            if(self.distancePlayerToObject(player,rival)< self.distanciaSegura):
                return True
        return False
    def nearestEnemy(self,player):
        nearest_distance_enemy=9999
        closest_rival=None
        for rival in self.rivals:
            distance_enemy=self.distancePlayerToObject(player,rival)
            if(distance_enemy<nearest_distance_enemy):
                nearest_distance_enemy=distance_enemy
                closest_rival=rival
        return closest_rival
    def getQuantityOfNearbyEnemiesPlayers(self,player):
        cant=0
        for rival in self.rivals:
            rival_distance=self.distancePlayerToObject(player,rival)
            if(rival_distance<self.distanciaSegura):
                cant=cant+1
        return cant
    def playerPositionInField(self,player):
        if(player.rect.centerx>AREA_G_MID_IZQ and player.rect.centerx<MITAD_CANCHA): #El jugador se encuentra entre el area izquierda y mitad de cancha
            return 1
        elif (player.rect.centerx>AREA_G_MID_DER): #El jugador se encuentra cerca del area derecha
            return 2
        elif (player.rect.centerx>MITAD_CANCHA and player.rect.centerx<AREA_G_MID_DER): #El jugador se encuentra entre el area derecha y mitad de cancha
            return 3
        else:#El jugador se encuentra cerca del area izquierda
            return 4


