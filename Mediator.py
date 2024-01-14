from players.GoalKeeper import GoalKeeper
from Constantes import *
import pygame, random


class Mediator(object):

    def __init__(self):
        self.ball = None
        self.players1 = pygame.sprite.Group()
        self.players2 = pygame.sprite.Group()
    def setBall(self, ball):
        self.ball = ball

    def addPlayer1(self, player):
        self.players1.add(player)

    def addPlayer2(self, player):
        self.players2.add(player)

    def restart_positions(self, team):
        self.ball.rect.center = (MITAD_CANCHA, SAQUE)
        # Equipo 1 hizo gol
        if team:
            i = 0
            for player in self.players2:
                if isinstance(player, GoalKeeper):
                    player.setPosition(POS_P5_F5)
                else:
                    if i == 0:
                        player.setPosition(POS_SAQUE)
                    else:
                        player.setPosition(POS_TEAM2_F5[i])
                    i += 1
            i = 0
            for player in self.players1:
                if isinstance(player, GoalKeeper):
                    player.setPosition(POS_P10_F5)
                else:
                    player.setPosition(POS_TEAM1_F5[i])
                    i += 1
        # Equipo 2 hizo gol
        else:
            i = 0
            for player in self.players1:
                if isinstance(player, GoalKeeper):
                    player.setPosition(POS_P10_F5)
                else:
                    if i == 0:
                        player.setPosition(POS_SAQUE)
                    else:
                        player.setPosition(POS_TEAM1_F5[i])
                    i += 1
            i = 0
            for player in self.players2:
                if isinstance(player, GoalKeeper):
                    player.setPosition(POS_P5_F5)
                else:
                    player.setPosition(POS_TEAM2_F5[i])
                    i += 1

    def restart_players_positions2(self):
        i = 0
        for player in self.players2:
            if isinstance(player, GoalKeeper):
                player.setPosition(POS_P5_F5)
            else:
                player.setPosition(POS_TEAM2_F5[i])
                i += 1
        i = 0
        for player in self.players1:
            if isinstance(player, GoalKeeper):
                player.setPosition(POS_P10_F5)
            else:
                player.setPosition(POS_TEAM1_F5[i])
                i += 1

    def restart_positions2(self, team):
        # Saca del arco equipo 1
        if team:
            self.ball.rect.center = (POS_P10_F5)
        # Saca del arco equipo 2
        else:
            self.ball.rect.center = (POS_P5_F5)
        self.restart_players_positions2()

    def check_collision_between_players(self, new_x, new_y, players):
        for teammate in players:
            if teammate is not self and not isinstance(teammate, GoalKeeper):
                player_distance = pygame.math.Vector2(teammate.rect.center) - pygame.math.Vector2(new_x, new_y)
                if player_distance.length() < 0:
                    return False
        return True

    def can_move(self, team, new_x, new_y):
        if team:
            return self.check_collision_between_players(new_x, new_y, self.players1)
        else:
            return self.check_collision_between_players(new_x, new_y, self.players2)

    def can_move2(self, team, player):
        if team:
            return pygame.sprite.spritecollide(player, self.players1, False)
        else:
            return pygame.sprite.spritecollide(player, self.players2, False)


    def check_collision_with_ball(self, player):
        if player.rect.colliderect(self.ball.rect):
            player.hasBall = True
            self.ball.rect.center = player.rect.center

    def check_collision_with_players(self):
        if pygame.sprite.spritecollide(self.ball, self.players1, False) or \
                pygame.sprite.spritecollide(self.ball, self.players2, False):
            return True
        return False

    def shot_ball(self, team):
        print(team)
        if team:
            self.ball.set_prox_pos(FONDO_DER, random.randint(PALO_SUP - 20, PALO_INF + 20))
        else:
            self.ball.set_prox_pos(FONDO_IZQ, random.randint(PALO_SUP - 20, PALO_INF + 20))


    def pass_ball(self, x, y):
        self.ball.set_prox_pos(x, y)

    # BORRAR
    def prueba(self):
        return self.ball.rect.centerx, self.ball.rect.centery

