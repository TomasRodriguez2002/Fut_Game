import pygame
from Constantes import *
import random

pygame.font.init()
font = pygame.font.Font(None, 100)

FPS = 30

# Dimensiones de pantalla
WIDTH = 1356
HEIGHT = 755

# Paleta de colores
AZUL = (0,0,255)

# Limites de la cancha
#...

class GoalKeeper(pygame.sprite.Sprite):

    def __init__(self, ball, team):
        super().__init__()

        self.image = pygame.image.load("player.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 485, self.image.get_height() - 485))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        self.team = team # True -> team1 | False -> team2
        if self.team:
            self.rect.center = (FONDO_IZQ+7, SAQUE)
        else:
            self.rect.center = (FONDO_DER-7, SAQUE)
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.velocidad = 7
        self.ball = ball
        self.hasBall = False
        self.teammates = []
        self.vision_angle = 126 # angulo de vision en función del ancho del arco
        self.vision_range = 223 # rango de visión en funcion de la distancia del comienzo del area grande con el arco
        self.direction = pygame.math.Vector2(1, 0) # direccion inicial hacia la derecha
    
    def update(self):
        self.velocidad= 7
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.vision_angle = 126
        self.vision_range = 1151 #223
        keys = pygame.key.get_pressed()

        # movimiento lateral
        if keys[pygame.K_LEFT]:
            self.velocidad_x = -self.velocidad
            self.direction = pygame.math.Vector2(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.velocidad_x = self.velocidad
            self.direction = pygame.math.Vector2(1, 0)

        # movimiento vertical
        if keys[pygame.K_UP]:
            self.velocidad_y = -self.velocidad
            self.direction = pygame.math.Vector2(0, -1)
        if keys[pygame.K_DOWN]:
            self.velocidad_y = self.velocidad
            self.direction = pygame.math.Vector2(0, 1)

        # Actualizar posición
        new_x = self.rect.x + self.velocidad_x
        new_y = self.rect.y + self.velocidad_y


        # Verificar límites laterales
        if AREA_G_SUP-7 < new_y < AREA_G_INF - self.rect.height+7:
            self.rect.y = new_y

        # Verificar límites de fondo
        if self.team:
            if FONDO_IZQ-5 < new_x < AREA_G_MID_IZQ - self.rect.width+5:
                self.rect.x = new_x
        else:
            if AREA_G_MID_DER-5 < new_x < FONDO_DER - self.rect.width+5:
                self.rect.x = new_x

        if self.rect.colliderect(self.ball.rect): #and (pygame.math.Vector2(self.rect.center).distance_to(self.ball.rect.center)) < (20):
            self.hasBall = True
            self.ball.rect.center = self.rect.center                
        
        if self.hasBall:
            # logica de movimiento con pelota
            self.ball.rect.x += self.velocidad_x
            self.ball.rect.y += self.velocidad_y

            # logica de visualizacion de companieros (nota: mas adelante puedo implementar que cada jugador se le pase
            # la lista solo con sus compañeros sin ellos incluidos (ver patron creacional))
            for teammate in self.teammates:
                teammate_vector = pygame.math.Vector2(teammate.rect.center)
                self_vector = pygame.math.Vector2(self.rect.center)
                direction_to_teammate = teammate_vector - self_vector
                distance_to_teammate = direction_to_teammate.length()
                #angulo entre el jugador y el companiero
                angle = direction_to_teammate.angle_to(self.direction) 
                if keys[pygame.K_SPACE]:
                    if distance_to_teammate <= self.vision_range and abs(angle) < self.vision_angle / 2:
                        # companiero dentro del rango y angulo de vision del jugador -> ejecutar pase
                        # (mas adelante debo considerar pasarsela a la mejor opcion (companiero mejor posicionado))
                        
                        self.ball.animate_pass(teammate.rect.centerx, teammate.rect.centery)
                        self.hasBall = False

    def addTeammate(self, teammate):   
        self.teammates.append(teammate)
        

class Player(pygame.sprite.Sprite):
    def __init__(self, coor_x, coor_y, ball, team):
        super().__init__()

        self.image = pygame.image.load("player.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 485, self.image.get_height() - 485))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        self.rect.center = (coor_x, coor_y)
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.ball = ball
        self.hasBall = False
        #self.vision_angle = 126 # angulo de vision en función del ancho del arco
        #self.vision_range = 223 # rango de visión en funcion de la distancia del comienzo del area grande con el arco
        #self.direction = pygame.math.Vector2(1, 0) # direccion inicial hacia la derecha
        self.teammates = []
        self.team = team

    def update(self):
        '''
        self.velocidad_x = 0
        self.velocidad_y = 0
        keys = pygame.key.get_pressed()
        # movimiento lateral
        if keys[pygame.K_a]:
            self.velocidad_x = -10
            self.direction = pygame.math.Vector2(-1, 0)
        if keys[pygame.K_d]:
            self.velocidad_x = 10
            self.direction = pygame.math.Vector2(1, 0)
        self.rect.x += self.velocidad_x
        # movimiento vertical
        if keys[pygame.K_w]:
            self.velocidad_y = -10
            self.direction = pygame.math.Vector2(0, -1)
        if keys[pygame.K_s]:
            self.velocidad_y = 10
            self.direction = pygame.math.Vector2(0, 1)
        self.rect.y += self.velocidad_y
        '''

        #self.vision_angle = 126
        #self.vision_range = 1151 #223

    
        velocidad_jugador= 7
        self.velocidad_x = 0
        self.velocidad_y = 0
        keys = pygame.key.get_pressed()

        # movimiento lateral
        if keys[pygame.K_a]:
            self.velocidad_x = -velocidad_jugador
            self.direction = pygame.math.Vector2(-1, 0)
        if keys[pygame.K_d]:
            self.velocidad_x = velocidad_jugador
            self.direction = pygame.math.Vector2(1, 0)

        # movimiento vertical
        if keys[pygame.K_w]:
            self.velocidad_y = -velocidad_jugador
            self.direction = pygame.math.Vector2(0, -1)
        if keys[pygame.K_s]:
            self.velocidad_y = velocidad_jugador
            self.direction = pygame.math.Vector2(0, 1)

        # Actualizar posición
        new_x = self.rect.x + self.velocidad_x
        new_y = self.rect.y + self.velocidad_y


        # Verificar límites laterales y de fondo
        if LATERAL_IZQ - 7 < new_y < LATERAL_DER - self.rect.height + 7 and FONDO_IZQ - 5 < new_x < FONDO_DER - self.rect.width + 5:
            # Verificar la distancia con los compañeros
            can_move = True
            for teammate in self.teammates:
                if not isinstance(teammate, GoalKeeper):
                    distancia_entre_jugadores = pygame.math.Vector2(teammate.rect.center) - pygame.math.Vector2(new_x, new_y)
                    if distancia_entre_jugadores.length() < (PALO_INF-SAQUE):
                        can_move = False
                        break

            if can_move:
                # Actualizar la posición solo si se puede mover
                self.rect.x = new_x
                self.rect.y = new_y


        '''
        for teammate in self.teammates:
            distancia_entre_jugadores = pygame.math.Vector2(teammate.rect.center) - pygame.math.Vector2(self.rect.center)
            print(distancia_entre_jugadores)
            if distancia_entre_jugadores.length() > (PALO_INF-SAQUE):
            
            if not self.rect.colliderect(teammate.rect):
                # Verificar límites laterales
                if LATERAL_IZQ-7 < new_y < LATERAL_DER - self.rect.height+7:
                    self.rect.y = new_y

                # Verificar límites de fondo
                if FONDO_IZQ-5 < new_x < FONDO_DER - self.rect.width+5:
                    self.rect.x = new_x
        '''
        # limites
        #if self.rect.left < FONDO_IZQ:
        #    self.rect = FONDO_IZQ:
        #...
        
        #si la distancia entre el jugador y la pelota es menor que 20 entonces el jugador tiene la pelota
        if self.rect.colliderect(self.ball.rect): #and (pygame.math.Vector2(self.rect.center).distance_to(self.ball.rect.center)) < (20):
            self.hasBall = True
            self.ball.rect.center = self.rect.center                
        
        if self.hasBall:
            # logica de movimiento con pelota
            self.ball.rect.x += self.velocidad_x
            self.ball.rect.y += self.velocidad_y

            # logica de visualizacion de companieros (nota: mas adelante puedo implementar que cada jugador se le pase
            # la lista solo con sus compañeros sin ellos incluidos (ver patron creacional))
            for teammate in self.teammates:
                '''
                teammate_vector = pygame.math.Vector2(teammate.rect.center)
                self_vector = pygame.math.Vector2(self.rect.center)
                direction_to_teammate = teammate_vector - self_vector
                distance_to_teammate = direction_to_teammate.length()
                #angulo entre el jugador y el companiero
                angle = direction_to_teammate.angle_to(self.direction)
                ''' 
                if keys[pygame.K_SPACE]:
                    #if distance_to_teammate <= self.vision_range and abs(angle) < self.vision_angle / 2:
                        # companiero dentro del rango y angulo de vision del jugador -> ejecutar pase
                        # (mas adelante debo considerar pasarsela a la mejor opcion (companiero mejor posicionado))
                        
                    self.ball.animate_pass(teammate.rect.centerx, teammate.rect.centery)
                    self.hasBall = False

            if keys [pygame.K_c]:
                if self.team:
                    self.ball.animate_pass(FONDO_DER, random.randint(PALO_SUP-10, PALO_INF+10))
                else:
                    self.ball.animate_pass(FONDO_IZQ, random.randint(PALO_SUP-10, PALO_INF+10))
                self.hasBall = False


    def addTeammate(self, teammate):   
        self.teammates.append(teammate)

class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        self.image = pygame.image.load("ball1.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 785, self.image.get_height() - 785))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2) 
        self.move_speed = 35
        self.is_moving = False
        #self.target_rect = self.rect.copy()
        self.dx = 0
        self.dy = 0
        self.distance = 0
        self.teammates = []
        self.player = None
        self.game = game

    def detect_goal(self):
        # Lógica para detectar si se marcó un gol
        # gol arco derecho -> saque del centro  
        if self.rect.left > 1252 and self.rect.top < 445 and self.rect.bottom > 317:
            self.rect.center = (677, 383)
            self.is_moving = False
            return True
        # gol arco izquierdo -> saque del centro
        if self.rect.right < 101 and self.rect.top < 445 and self.rect.bottom > 317:
            self.rect.center = (677, 383)
            self.is_moving = False
            return True
        return False

    def update(self):

        if self.detect_goal():
            self.game.show_goal_message("¡Goooaaal!", 25)  # Ajusta la duración según sea necesario
        
        # Si la posición en y de la pelota supera algun lateral -> efecto rebote en y
        if self.rect.top <= 48 or self.rect.bottom >= 719:
            #if self.is_moving:
            self.dy *= -1
        
        # Si la posición en y de la pelota no se encuentra entre los palos y la posicion en x supera la linea de fondo (der o izq) -> efecto rebote en x 
        if (self.rect.bottom >= 445 or self.rect.top <= 317) and (self.rect.left <= 101 or self.rect.right >= 1252):
            self.dx *= -1
         
        '''

        if self.is_moving:
            dx = self.target_rect.centerx - self.rect.centerx
            dy = self.target_rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > self.move_speed:
                self.rect.x += dx / distance * self.move_speed
                self.rect.y += dy / distance * self.move_speed
                
            else:
                self.is_moving = False
                self.rect.center = self.target_rect.center

        '''

        if self.is_moving:
            if self.move_speed != 0 and self.distance != 0:
                self.rect.x += self.dx / self.distance * self.move_speed
                self.rect.y += self.dy / self.distance * self.move_speed
                self.move_speed -= 1
            if self.move_speed <= 0 or pygame.sprite.spritecollide(self, self.teammates, False):#or self.rect.collidedictall(self.teammates):
                self.move_speed = 35
                self.is_moving = False
                
                
    '''
    def animate_pass(self, player_rect_center):
        self.target_rect.center = player_rect_center
        self.is_moving = True
    '''

    def animate_pass(self, player_rect_centerx, player_rect_centery):
        self.dx = player_rect_centerx - self.rect.centerx
        self.dy = player_rect_centery - self.rect.centery
        self.distance = (self.dx ** 2 + self.dy ** 2) ** 0.5
        self.is_moving = True
    

    def addTeammate(self, teammate):   
        self.teammates.append(teammate)


class Game(object):

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.initialize_game()

    def initialize_game(self):
        self.sprites = pygame.sprite.Group()
        self.ball = Ball(self)
        self.player1 = Player((WIDTH // 2)-200, (HEIGHT // 2)-200, self.ball, True)
        self.player2 = Player((WIDTH // 2), (HEIGHT // 2)-200, self.ball, True)
        self.player3 = Player((WIDTH // 2)-200, (HEIGHT // 2), self.ball, True)
        self.goalkeeper1 = GoalKeeper(self.ball, True)        
        self.goal_message = None         
        self.current_goal_message = None
        self.player1.addTeammate(self.player2)
        self.player1.addTeammate(self.player3)
        self.player1.addTeammate(self.goalkeeper1)
        self.player2.addTeammate(self.player1)
        self.player2.addTeammate(self.player3)
        self.player2.addTeammate(self.goalkeeper1)
        self.player3.addTeammate(self.player1)
        self.player3.addTeammate(self.player2)
        self.player3.addTeammate(self.goalkeeper1)
        self.goalkeeper1.addTeammate(self.player1)
        self.goalkeeper1.addTeammate(self.player2)
        self.goalkeeper1.addTeammate(self.player3)
        self.ball.addTeammate(self.player1)
        self.ball.addTeammate(self.player2)
        self.ball.addTeammate(self.player3)
        self.ball.addTeammate(self.goalkeeper1)
        self.sprites.add(self.player1)
        self.sprites.add(self.player2)
        self.sprites.add(self.player3)
        self.sprites.add(self.goalkeeper1)
        self.sprites.add(self.ball)

    def reset_game(self):
        self.sprites.empty()  # Elimina todos los sprites actuales
        self.initialize_game()
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                # Verificar si se presionó Ctrl+R para resetear el juego
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.reset_game()
        return False

    def run_logic(self):
        self.sprites.update()

    def display_frame(self, screen, background):
        screen.blit(background, [0 , 0])
        self.sprites.draw(screen)
        if self.current_goal_message:
            screen.blit(self.current_goal_message, ((WIDTH - self.current_goal_message.get_width()) // 2, HEIGHT // 2))
            # Reduzca el temporizador del mensaje de gol en cada iteración
            self.goal_message_timer -= 1
            if self.goal_message_timer <= 0:
                self.current_goal_message = None  # Borra el mensaje cuando el temporizador llega a cero
        pygame.display.flip()

    def show_goal_message(self, message, duration):
            self.goal_message_timer = duration
            self.current_goal_message = font.render(message, True, (255, 255, 255))  # Color blanco


def main():
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])#, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False
    background = pygame.image.load("estadio2.png").convert() 
    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen, background)
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
