import pygame

FPS = 30

# Dimensiones de pantalla
WIDTH = 1356
HEIGHT = 755

# Paleta de colores
AZUL = (0,0,255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #self.image = pygame.Surface((20, 20))
        #self.image.fill(AZUL)
        self.image = pygame.image.load("player.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 470, self.image.get_height() - 470))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH // 2)-200, HEIGHT // 2) 

    def update(self):
        self.rect.x += 10
        self.rect.y -= 5

        if  self.rect.left > WIDTH:
            self.rect.center = ((WIDTH // 2)-200, HEIGHT // 2)
        

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("ball1.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 780, self.image.get_height() - 780))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2) 

    def update(self):
        self.rect.x += 10
        #if self.rect.left > WIDTH:
            #self.rect.right = 0
        
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

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
clock = pygame.time.Clock()
done = False
background = pygame.image.load("estadio2.png").convert()

sprites = pygame.sprite.Group()
player = Player()
ball = Ball()
sprites.add(player)
sprites.add(ball)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    clock.tick(FPS)

    screen.blit(background, [0 , 0])

    sprites.update()
    sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()