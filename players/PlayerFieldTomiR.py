from IPlayerField import IPlayerField
import pygame

class PlayerFieldNicolas(IPlayerField, pygame.sprite.Sprite):

    def __init__(self, coor_x, coor_y):
        self.image = pygame.image.load("player.png").convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 480, self.image.get_height() - 480))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        self.rect.center = (coor_x, coor_y)
        #self.velocidad_x = 0
        #self.velocidad_y = 0
        #self.ball = ball
        #self.hasBall = False
        #self.vision_angle = 126 # angulo de vision en función del ancho del arco
        #self.vision_range = 223 # rango de visión en funcion de la distancia del comienzo del area grande con el arco
        #self.direction = pygame.math.Vector2(1, 0) # direccion inicial hacia la derecha
        #self.teammates = []

    def update(self):
        pass