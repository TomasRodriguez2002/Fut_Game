from players.GoalKeeper import GoalKeeper
from Constantes import *
import pygame, random

class Mediator(object):

    def __init__(self):
        self.ball = None
        self.players1 = []
        self.players2 = []

    def setBall(self, ball):
        self.ball = ball

    def addPlayer1(self, player):
        self.players1.add(player)

    def addPlayer1(self, player):
        self.players2.add(player)

    def check_collision_between_players(self, new_x, new_y, players):
        for teammate in players:
            if not isinstance(teammate, GoalKeeper):
                distancia_entre_jugadores = pygame.math.Vector2(teammate.rect.center) - pygame.math.Vector2(new_x, new_y)
                if distancia_entre_jugadores.length() < (PALO_INF-SAQUE):
                    return False
        return True

    def can_move(self, team, new_x, new_y):
        if team:
            return self.check_collision_between_players(new_x, new_y, self.players1)
        else:    
            return self.check_collision_between_players(new_x, new_y, self.players2)
        
    def check_collision_with_ball(self, player):
        if player.rect.colliderect(self.ball.rect):
            player.hasBall = True
            self.ball.rect.center = player.rect.center

    def shot_ball(self, team):
        if team:
            self.ball.set_prox_pos(FONDO_DER, random.randint(PALO_SUP-20, PALO_INF+20))
        else:
            self.ball.set_prox_pos(FONDO_IZQ, random.randint(PALO_SUP-20, PALO_INF+20))

    def pass_ball(self, x, y):
        self.ball.set_prox_pos(x, y)
