from players.GoalKeeper import GoalKeeper
from Constantes import *
import pygame, random

class Mediator(object):

    def __init__(self):
        self.ball = None
        self.players1 = pygame.sprite.Group()
        self.players2 = pygame.sprite.Group()
        self.pinch = False
        self.pass_sound = pygame.mixer.Sound("Sounds/pass.wav")
        self.pass_sound.set_volume(0.7)
        self.shot_sound = pygame.mixer.Sound("Sounds/shot.wav")

    def setBall(self, ball):
        self.ball = ball

    def addPlayer1(self, player):
        self.players1.add(player)

    def addPlayer2(self, player):
        self.players2.add(player)

    def restart_positions(self, team):
        self.ball.game.whistle.play()
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

    def restart_players_positions_to_goal_kick(self):
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

    # boolean fondo (True == fondo izq | False == fondo der)
    def restart_positions_to_goal_kick(self, fondo):
        self.ball.game.whistle.play()
        # Saca del arco equipo 1
        if fondo:
            self.ball.rect.center = (POS_P10_F5)
        # Saca del arco equipo 2
        else:
            self.ball.rect.center = (POS_P5_F5)
        self.restart_players_positions_to_goal_kick()

    def restart_players_positions_to_lateral_izq_team1(self):
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
            # jugador P8 saca lateral
            elif i == 2:
                player.rect.centerx, player.rect.centery = self.ball.rect.centerx, LATERAL_IZQ+7
                pos_teammate = self.players1.sprites()[0].rect.center
                self.pass_ball(pos_teammate[0], pos_teammate[1])
                i +=1
            else:
                player.setPosition(POS_TEAM1_F5[i])
                i += 1

    def restart_players_positions_to_lateral_der_team1(self):
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
            # jugador P8 saca lateral
            elif i == 2:
                player.rect.centerx, player.rect.centery = self.ball.rect.centerx, LATERAL_DER-7
                pos_teammate = self.players1.sprites()[0].rect.center
                self.pass_ball(pos_teammate[0], pos_teammate[1])
                i +=1
            else:
                player.setPosition(POS_TEAM1_F5[i])
                i += 1

    def restart_players_positions_to_lateral_izq_team2(self):
        i = 0
        for player in self.players2:
            if isinstance(player, GoalKeeper):
                player.setPosition(POS_P5_F5)
            # jugador P3 saca lateral
            elif i == 2:
                player.rect.centerx, player.rect.centery = self.ball.rect.centerx, LATERAL_IZQ+7
                pos_teammate = self.players2.sprites()[0].rect.center
                self.pass_ball(pos_teammate[0], pos_teammate[1])
                i +=1
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

    def restart_players_positions_to_lateral_der_team2(self):
        i = 0
        for player in self.players2:
            if isinstance(player, GoalKeeper):
                player.setPosition(POS_P5_F5)
            # jugador P3 saca lateral
            elif i == 2:
                player.rect.centerx, player.rect.centery = self.ball.rect.centerx, LATERAL_DER-7
                pos_teammate = self.players2.sprites()[0].rect.center
                self.pass_ball(pos_teammate[0], pos_teammate[1])
                i +=1
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

    # boolean mitad_cancha (True == mitad de cancha de team1 | False == mitad de cancha de team2)
    # boolean lateral (True == lateral izq, es decir, arriba  | False == lateral der, es decir, abajo)
    def restart_positions_to_lateral(self, mitad_cancha, lateral):
        self.ball.game.whistle.play()
        if mitad_cancha:
            # lateral izq en mitad de cancha team1
            if lateral:
                self.ball.rect.centery = LATERAL_IZQ
                self.restart_players_positions_to_lateral_izq_team1()
            # lateral der en mitad de cancha team1 
            else:
                self.ball.rect.centery = LATERAL_DER
                self.restart_players_positions_to_lateral_der_team1()
        # lateral izq en mitad de cancha team2
        elif lateral:
            self.ball.rect.centery = LATERAL_IZQ
            self.restart_players_positions_to_lateral_izq_team2()
        # lateral der en mitad de cancha team2
        else:
            self.ball.rect.centery = LATERAL_DER
            self.restart_players_positions_to_lateral_der_team2()        

    '''
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
    
            
    def can_move(self, team, player):
        if team:
            return pygame.sprite.spritecollide(player, self.players1, False)
        else:
            return pygame.sprite.spritecollide(player, self.players2, False)
    '''

    def check_collision_with_ball(self, player):
        if player.rect.colliderect(self.ball.rect) and not self.pinch:
            player.hasBall = True
            self.ball.rect.center = player.rect.center
            '''
            if player.direction_of_movement == "R":
                self.ball.rect.left = player.rect.right
                self.ball.rect.centery = player.rect.centery
            elif player.direction_of_movement == "L":
                self.ball.rect.right = player.rect.left
                self.ball.rect.centery = player.rect.centery
            elif player.direction_of_movement == "B":
                self.ball.rect.top = player.rect.bottom
                self.ball.rect.centerx = player.rect.centerx
            elif player.direction_of_movement == "T":
                self.ball.rect.bottom = player.rect.top
                self.ball.rect.centerx = player.rect.centerx
            elif player.direction_of_movement == "RB":
                self.ball.rect.left = player.rect.right
                self.ball.rect.top = player.rect.bottom
            elif player.direction_of_movement == "RT":
                self.ball.rect.left = player.rect.right
                self.ball.rect.bottom = player.rect.top
            elif player.direction_of_movement == "LB":
                self.ball.rect.right = player.rect.left
                self.ball.rect.top = player.rect.bottom
            elif player.direction_of_movement == "LT":
                self.ball.rect.right = player.rect.left
                self.ball.rect.bottom = player.rect.top
            '''
        else:
            player.hasBall = False

    def check_collision_with_players(self):
        if pygame.sprite.spritecollide(self.ball, self.players1, False) or \
                pygame.sprite.spritecollide(self.ball, self.players2, False):
            return True
        return False

    def shot_ball(self, team):
        if team:
            self.ball.set_prox_pos(FONDO_DER, random.randint(PALO_SUP - 20, PALO_INF + 20))
        else:
            self.ball.set_prox_pos(FONDO_IZQ, random.randint(PALO_SUP - 20, PALO_INF + 20))
        self.shot_sound.play()

    def pass_ball(self, x, y):
        self.ball.set_prox_pos(x, y)
        self.pass_sound.play()
    
    def getTeammates(self, team):
        if team:
            return self.players1
        else:
            return self.players2
    
    def getRivals(self, team):
        if team:
            return self.players2
        else:
            return self.players1
        
    def getBallsPosition(self):
        return self.ball.rect.centerx, self.ball.rect.centery

    def fighting_for_ball(self):
        cont1 = 0
        cont2 = 0
        for player in self.players1:
            if player.rect.colliderect(self.ball):
                cont1+=1

        for player in self.players2:
            if player.rect.colliderect(self.ball):
                cont2+=1

        if (cont1 > 0 and cont2 > 0) or (cont1 > 1) or (cont2 > 1):
            self.pinch = True
            random_x = random.randint(FONDO_IZQ,FONDO_DER)
            random_y = random.randint(LATERAL_IZQ,LATERAL_DER)
            self.ball.set_prox_pos(random_x, random_y)
            self.shot_sound.play()
        else:
            self.pinch = False
