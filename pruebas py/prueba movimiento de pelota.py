import pygame

FPS = 30

# Dimensiones de pantalla
WIDTH = 1356
HEIGHT = 755

# Paleta de colores
AZUL = (0,0,255)

# Limites de la cancha
#...

class Player(pygame.sprite.Sprite):
    def __init__(self, coor_x, coor_y, ball):
        super().__init__()

        self.image = pygame.image.load("player.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 480, self.image.get_height() - 480))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        self.rect.center = (coor_x, coor_y)
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.ball = ball
        self.hasBall = False
        self.vision_angle = 126 # angulo de vision en función del ancho del arco
        self.vision_range = 223 # rango de visión en funcion de la distancia del comienzo del area grande con el arco
        self.direction = pygame.math.Vector2(1, 0) # direccion inicial hacia la derecha
        self.teammates = []

    def update(self):
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
        
        self.vision_angle = 126
        self.vision_range = 223

        # limites
        #if self.rect.left < FONDO_IZQ:
        #    self.rect = FONDO_IZQ:
        #...
        
        #si la distancia entre el jugador y la pelota es menor que 20 entonces el jugador tiene la pelota
        if (pygame.math.Vector2(self.rect.center).distance_to(self.ball.rect.center)) < (20):
            self.hasBall = True
        else:
            self.hasBall = False                
        
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
                if distance_to_teammate <= self.vision_range and abs(angle) < self.vision_angle / 2:
                    # companiero dentro del rango y angulo de vision del jugador -> ejecutar pase
                    # (mas adelante debo considerar pasarsela a la mejor opcion (companiero mejor posicionado))
                    self.ball.animate_pass(teammate.rect.center)

    def addTeammate(self, teammate):   
        if isinstance(teammate, Player):
            if teammate != self:
                self.teammates.append(teammate)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("ball1.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 785, self.image.get_height() - 785))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2) 
        self.move_speed = 30
        self.is_moving = False
        self.target_rect = self.rect.copy()
        self.teammates = []

    def update(self):
        #self.rect.x += 10
        
        # gol arco derecho -> saque del centro
        if self.rect.left > 1254 and self.rect.top < 444 and self.rect.bottom > 320:
            self.rect.center = (WIDTH // 2, HEIGHT // 2)

        # gol arco izquierdo -> saque del centro
        if self.rect.left < 103 and self.rect.top < 444 and self.rect.bottom > 320:
            self.rect.center = (WIDTH // 2, HEIGHT // 2)

        #implementar logica para laterales y corners
            
        '''
        1254 x 444 (arco der palo de abajo)
        1254 x 320 (arco der palo de arriba)

        103 x 444 (arco der palo de abajo)
        103 x 320 (arco der palo de arriba)
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

    def animate_pass(self, player_rect_center):
        self.target_rect.center = player_rect_center
        self.is_moving = True

    def addTeammate(self, teammate):   
        if isinstance(teammate, Player):
            if teammate != self:
                self.teammates.append(teammate)


class Game(object):

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.player1 = Player((WIDTH // 2)-200, (HEIGHT // 2)-200, self.ball)
        self.player2 = Player((WIDTH // 2)+23, (HEIGHT // 2)-200, self.ball)
        self.player1.addTeammate(self.player2)
        self.player2.addTeammate(self.player1)
        self.ball.addTeammate(self.player1)
        self.ball.addTeammate(self.player2)
        self.sprites.add(self.player1)
        self.sprites.add(self.player2)
        self.sprites.add(self.ball)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def run_logic(self):
        self.sprites.update()

    def display_frame(self, screen, background):
        screen.blit(background, [0 , 0])
        self.sprites.draw(screen)
        pygame.display.flip()

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
