import math
import threading
import pygame

from Strategies.Strategy import Strategy
from Constantes import *
import random

from players.GoalKeeper import GoalKeeper


class TomasGStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.marked_opponents = {}
        self.marked_opponents_lock = threading.Lock()
        #self.marked_rivals_true = {}
        #self.marked_rivals_false = {}

    def is_goalkeeper_closest_to_ball(self, player, teammates):
        ball_position = self.mediator.getBallsPosition()
        outfield_teammates = [teammate for teammate in teammates if not isinstance(teammate, GoalKeeper)]
        if outfield_teammates:
            distances_to_teammates = [self.get_distance2(teammate, ball_position) for teammate in outfield_teammates]
            distance_to_goalkeeper = self.get_distance2(player, ball_position)
            if distance_to_goalkeeper < min(distances_to_teammates):
                return True
            else:
                return False
        else:
            return True
    def getProxPos(self, player):
        ball_position = self.mediator.getBallsPosition()
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)
        if isinstance(player, GoalKeeper):

            if player.team:
                if AREA_G_MID_IZQ > ball_position[0] > FONDO_IZQ and AREA_G_SUP < ball_position[1] < AREA_G_INF:
                    if self.is_goalkeeper_closest_to_ball(player,teammates):
                        return ball_position
                    else:
                        return POS_P10_F5
                else:
                    rival_with_ball = next((rival for rival in rivals if rival.hasBall), None)
                    if rival_with_ball:
                        current_position = POS_P10_F5
                        small_range = 200
                        new_y = current_position[1] + random.randint(-small_range, small_range)
                        return current_position[0], new_y
                    return POS_P10_F5
            else:
                if AREA_G_MID_DER < ball_position[0] < FONDO_DER and AREA_G_SUP < ball_position[1] < AREA_G_INF:
                    if self.is_goalkeeper_closest_to_ball(player, teammates):
                        return ball_position
                    else:
                        return POS_P5_F5
                else:
                    rival_with_ball = next((rival for rival in rivals if rival.hasBall), None)
                    if rival_with_ball:
                        current_position = POS_P5_F5
                        small_range = 200
                        new_y = current_position[1] + random.randint(-small_range, small_range)
                        return current_position[0], new_y
                    return POS_P5_F5
        else:
            if player.hasBall:
                # Si el jugador tiene la pelota, dirigirse hacia el área del equipo rival
                if player.team:
                    return AREA_G_MID_DER, player.rect.centery
                else:
                    return AREA_G_MID_IZQ, player.rect.centery
            else:
                # Verificar si algún compañero de equipo tiene la pelota
                teammate_with_ball = next((teammate for teammate in teammates if teammate.hasBall), None)

                if teammate_with_ball:
                    #print("Mi compañero tiene la pelota")
                    # Obtener la posición del compañero con pelota
                    teammate_position = teammate_with_ball.rect.center

                    # Calcular nueva posición alejada de los rivales
                    new_pos = self.calculate_position_away_from_rivals(teammate_position, teammates, player)
                    #print("Alejarse de los rivales")
                    return new_pos

                if not any(teammate.hasBall for teammate in teammates):
                    # Obtener la posición de la pelota
                    ball_position = self.mediator.getBallsPosition()

                    # Filtrar los compañeros de equipo que no son arqueros
                    outfield_teammates = [teammate for teammate in teammates if not isinstance(teammate, GoalKeeper)]

                    if outfield_teammates:
                        # Calcular las distancias de los jugadores de tu equipo no arqueros a la pelota
                        distances_to_teammates = [self.get_distance2(teammate, ball_position) for teammate in
                                                  outfield_teammates]

                        # Encontrar al jugador de tu equipo no arquero más cercano a la pelota
                        closest_teammate = outfield_teammates[distances_to_teammates.index(min(distances_to_teammates))]

                        # Si el jugador actual es el más cercano al compañero de tu equipo con la pelota, ir a quitarla
                        if closest_teammate == player:
                            return ball_position
                        else:
                            if player.team:

                                # Lógica para marcar a los rivales que se dirigen al arco derecho
                                opposing_players = [opponent for opponent in rivals if
                                                    opponent.rect.x > ball_position[0]] #ARREGLAR ESTA PARTEeeeeeeeeeeeeeeeeeeee
                                with self.marked_opponents_lock:
                                    print("HGola")
                                    unmarked_opponents = [opp for opp in opposing_players if
                                                          opp not in self.marked_opponents.values()]
                                    if unmarked_opponents:
                                        closest_opponent = min(unmarked_opponents,
                                                               key=lambda opp: self.get_distance2(player, opp.rect.center))
                                        self.marked_opponents[
                                            player] = closest_opponent  # Marcar al oponente para evitar que otros jugadores lo elijan

                                        return closest_opponent.rect.center
                            else:
                                # Lógica para marcar a los rivales que se dirigen al arco izquierdo
                                opposing_players = [opponent for opponent in rivals if
                                                    opponent.rect.x < ball_position[0]]
                                with self.marked_opponents_lock:
                                    unmarked_opponents = [opp for opp in opposing_players if
                                                          opp not in self.marked_opponents.values()]
                                    if unmarked_opponents:
                                        closest_opponent = min(unmarked_opponents,
                                                               key=lambda opp: self.get_distance2(player, opp.rect.center))
                                        self.marked_opponents[
                                            player] = closest_opponent  # Marcar al oponente para evitar que otros jugadores lo elijan

                                        return closest_opponent.rect.center

            #print("Me mantengo quieto")
            # Obtener la posición actual del jugador

            #El mas lejos a la pelota que mantenga su posicion atras de mitad de cancha y los demas van a presionar a los rivales mas cercanos a la pelota.
            current_position = player.rect.center
            small_range = 10
            new_x = current_position[0] + random.randint(-small_range, +small_range)
            new_y = current_position[1] + random.randint(-small_range, +small_range)
            return new_x, new_y



    def calculate_position_away_from_rivals(self, target_position, teammates, player):
        # Filtrar los compañeros de equipo que no son arqueros
        outfield_teammates = [teammate for teammate in teammates if not isinstance(teammate, GoalKeeper)]

        if outfield_teammates:
            # Calcular las distancias de los jugadores de tu equipo no arqueros a la pelota
            distances_to_teammates = [self.get_distance2(teammate, target_position) for teammate in outfield_teammates]
            teammate_lejos = outfield_teammates[distances_to_teammates.index(max(distances_to_teammates))]
            small_range = 100
            if teammate_lejos == player:
                if player.team:
                    new_x = AREA_G_MID_IZQ + random.uniform(-small_range, small_range)
                    new_y = SAQUE + random.uniform(-small_range, small_range)
                    new_position = (new_x, new_y)
                else:
                    new_x = AREA_G_MID_DER + random.uniform(-small_range, small_range)
                    new_y = SAQUE + random.uniform(-small_range, small_range)
                    new_position = (new_x, new_y)
            else:
                small_range = 270
                if player.team:
                    new_x = AREA_G_MID_DER + random.uniform(-small_range, small_range)
                    new_y = SAQUE + random.uniform(-small_range, small_range)
                    new_position = (new_x, new_y)
                else:
                    new_x = AREA_G_MID_IZQ + random.uniform(-small_range, small_range)
                    new_y = SAQUE + random.uniform(-small_range, small_range)
                    new_position = (new_x, new_y)

            return new_position

        return player.rect.centerx, player.rect.centery

    def move_towards_goal(self, x, y):
        # Lógica para mover hacia la posición deseada
        # Implementa según tus necesidades específicas
        return (x, y)

    def with_ball(self, player):
        # Obtener información sobre la posición del jugador, compañeros de equipo y rivales
        player_position = (player.rect.centerx, player.rect.centery)
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)
        # Ejemplo: Si el jugador está cerca del área del equipo contrario, dispara al arco
        if player.team and player.rect.centerx >= AREA_G_MID_DER - 120:
            return 1
        elif not player.team and player.rect.centerx <= AREA_G_MID_IZQ + 120:
            return 1
        else:

            # Ejemplo: Si hay rivales cerca, mueve el balón para evitar pérdidas
            if rivals:
                # Obtener el rival más cercano
                closest_rival = min(rivals.sprites(), key=lambda rival: self.get_distance(player, rival))

                # Ejemplo: Si el rival más cercano está en una posición para interceptar, mueve el balón
                if self.get_distance(player, closest_rival) < 100:
                    return 3

            # Ejemplo: Si hay compañeros de equipo cerca, pasa la pelota
            if teammates:
                # Obtener el jugador más cercano entre los compañeros de equipo
                closest_teammate = min(teammates.sprites(),
                                       key=lambda teammate: self.get_distance(player, teammate))

                # Ejemplo: Si el compañero de equipo más cercano está en una posición para recibir un pase, realiza el pase
                if self.get_distance(player, closest_teammate) < 25:
                    return 2

        # Si no se cumple ninguna condición anterior, mueve con la pelota
        return 3

    def get_distance(self, player1, player2):
        # Calcular la distancia euclidiana entre dos jugadores
        return pygame.math.Vector2(player1.rect.center).distance_to(player2.rect.center)

    def get_distance2(self, player, target_position):
        # Utilizar Vector2 para calcular la distancia entre el jugador y la posición objetivo
        player_position = pygame.math.Vector2(player.rect.center)
        target_position = pygame.math.Vector2(target_position)
        return player_position.distance_to(target_position)

    def where_to_pass(self, player):
        teammates = self.mediator.getTeammates(player.team)
        if teammates:
            # Inicializar el jugador más cercano y su distancia
            closest_teammate = None
            closest_distance = float('inf')

            # Iterar sobre los compañeros de equipo y encontrar el más cercano
            for teammate in teammates.sprites():
                # Omitir el jugador actual en la comparación
                if teammate != player:
                    distance = self.get_distance(player, teammate)
                    if distance < closest_distance:
                        closest_teammate = teammate
                        closest_distance = distance

            # Verificar si el jugador más cercano está a menos de 50 pixeles
            if closest_teammate and closest_distance < 100:
                # Buscar otro compañero de equipo al cual pasarle la pelota
                for other_teammate in teammates.sprites(): #TENDRIA QUE BUSCAR AL PROXIMO MAS CERCANO CREO.
                    if other_teammate != player and other_teammate != closest_teammate:
                        return other_teammate.rect.centerx, other_teammate.rect.centery

            # Si se encontró un compañero de equipo, devolver las coordenadas
            if closest_teammate:
                return closest_teammate.rect.centerx, closest_teammate.rect.centery

        # Si no hay compañeros de equipo, o todos están muy lejos, regresar None o alguna posición por defecto
        return None