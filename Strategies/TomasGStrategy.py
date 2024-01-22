
import pygame
from Strategies.Strategy import Strategy
from Constantes import *
import random

from players.GoalKeeper import GoalKeeper


class TomasGStrategy(Strategy):
    def __init__(self):
        super().__init__()

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
                if player.hasBall:
                    return AREA_G_MID_IZQ - player.rect.width+5,player.rect.centery
                else:
                    if AREA_G_MID_IZQ - player.rect.width + 5 > ball_position[0] > FONDO_IZQ and AREA_G_SUP-7 < ball_position[1] < AREA_G_INF - player.rect.height+7:
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
                if player.hasBall:
                    return AREA_G_MID_DER + 5, player.rect.centery
                else:
                    if AREA_G_MID_DER + 5 < ball_position[0] < FONDO_DER - player.rect.width + 5 and AREA_G_SUP-7 < ball_position[1] < AREA_G_INF - player.rect.height+7:
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
                new_y = player.rect.centery + random.uniform(-150, 150)
                if player.team:
                    return AREA_G_MID_DER, new_y
                else:
                    return AREA_G_MID_IZQ, new_y
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

            # Obtener la posición actual del jugador
            #El mas lejos a la pelota que mantenga su posicion atras de mitad de cancha y los demas van a presionar a los rivales mas cercanos a la pelota.
            if player.team:
                if ball_position[0] < MITAD_CANCHA:
                    current_position = player.rect.center
                    if 50 < self.get_distance2(player, ball_position) < 200:
                        return ball_position
                    new_x = AREA_G_MID_IZQ
                    small_range = 300
                    new_y = current_position[1] + random.randint(-small_range, +small_range)
                    return new_x, new_y
                else:              #teammate_cercano_ball = min(teammates.sprites(), key=lambda teammate: self.get_distance2(teammate, ball_position))
                    current_position = player.rect.center
                    small_range = 100
                    new_x = AREA_G_MID_IZQ+100 + random.randint(-small_range, +small_range)
                    small_range = 300
                    new_y = current_position[1] + random.randint(-small_range, +small_range)
                    return new_x, new_y
            else:
                if ball_position[0] > MITAD_CANCHA:
                    if 50 < self.get_distance2(player, ball_position) < 200:
                        return ball_position
                    current_position = player.rect.center
                    new_x = AREA_G_MID_DER
                    small_range = 300
                    new_y = current_position[1] + random.randint(-small_range, +small_range)
                    return new_x, new_y
                else:  # teammate_cercano_ball = min(teammates.sprites(), key=lambda teammate: self.get_distance2(teammate, ball_position))
                    current_position = player.rect.center
                    small_range = 100
                    new_x = AREA_G_MID_IZQ + 100 + random.randint(-small_range, +small_range)
                    small_range = 300
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
                small_range = 200
                if player.team:
                    new_x = AREA_G_MID_DER + random.randint(0,small_range)
                    new_y = player.rect.centery + random.uniform(-small_range, small_range)
                    new_position = (new_x, new_y)
                else:
                    new_x = AREA_G_MID_IZQ + random.randint(-small_range,0)
                    new_y = player.rect.centery + random.uniform(-small_range, small_range)
                    new_position = (new_x, new_y)

            return new_position

        return player.rect.centerx, player.rect.centery


    def closses_teammate_in_area(self,player,teammates):
        if player.team:
            closest_teammate = min(teammates.sprites(),
                                   key=lambda teammate: self.get_distance(player,
                                teammate) if teammate.rect.centerx >= AREA_G_MID_DER - 130 else float('inf'))
            return closest_teammate
        else:
            closest_teammate = min(teammates.sprites(),
                                   key=lambda teammate: self.get_distance(player,
                                                                          teammate) if teammate.rect.centerx <= AREA_G_MID_IZQ + 130 else float('inf'))
            return closest_teammate

    def with_ball(self, player):
        # Obtener información sobre la posición del jugador, compañeros de equipo y rivales
        player_position = (player.rect.centerx, player.rect.centery)
        teammates = self.mediator.getTeammates(player.team)
        rivals = self.mediator.getRivals(player.team)
        # Ejemplo: Si el jugador está cerca del área del equipo contrario, dispara al arco
        if player.team and player.rect.centerx >= AREA_G_MID_DER - 80:
            return 1
        elif not player.team and player.rect.centerx <= AREA_G_MID_IZQ + 80:
            return 1
        else:
            closest_rival = min(rivals.sprites(), key=lambda rival: self.get_distance(player, rival))
            closest_teammate = min(teammates.sprites(),
                                   key=lambda teammate: self.get_distance(player, teammate))
            if player.hasBall:
                if self.get_distance(player,closest_rival) < 50:
                    return 2
            # Ejemplo: Si hay compañeros de equipo cerca, pasa la pelota
            if player.team:
                closest_teammate_in_area = self.closses_teammate_in_area(player, teammates)
                if not isinstance(player,GoalKeeper) and player.rect.centerx >= AREA_G_MID_DER - 200 and closest_teammate_in_area.rect.centerx > player.rect.centerx:

                    return 2
                else:
                    if isinstance(player, GoalKeeper):
                        return 2
            else:
                closest_teammate_in_area = self.closses_teammate_in_area(player, teammates)
                if not isinstance(player,GoalKeeper) and player.rect.centerx <= AREA_G_MID_IZQ + 200 and closest_teammate_in_area.rect.centerx < player.rect.centerx:

                    return 2
                else:
                    if isinstance(player, GoalKeeper):
                        return 2

            if teammates:
                # Ejemplo: Si el compañero de equipo más cercano está en una posición para recibir un pase, realiza el pase
                if (self.get_distance(player, closest_teammate) > 15 and not self.player_collision_rival(closest_teammate,closest_rival)) or self.get_distance(player,closest_rival) < 15:
                    return 2

            # Ejemplo: Si hay rivales cerca, mueve el balón para evitar pérdidas
            if rivals:

                if self.get_distance(player, closest_rival) > 25:
                    return 3

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

    def player_collision_rival(self, player, rival):
        rect_player = player.rect
        rect_rival = rival.rect
        if rect_player.colliderect(rect_rival):
            return True
        return False

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
            if closest_teammate and closest_distance < 100 and not self.player_collision_rival(player,closest_teammate):
                # Buscar otro compañero de equipo al cual pasarle la pelota
                for other_teammate in teammates.sprites(): #TENDRIA QUE BUSCAR AL PROXIMO MAS CERCANO CREO.
                    if other_teammate != player and other_teammate != closest_teammate and not self.player_collision_rival(player,other_teammate):
                        return other_teammate.rect.centerx, other_teammate.rect.centery

            # Si se encontró un compañero de equipo, devolver las coordenadas
            if closest_teammate:
                return closest_teammate.rect.centerx, closest_teammate.rect.centery

        # Si no hay compañeros de equipo, o todos están muy lejos, regresar None o alguna posición por defecto
        return None
