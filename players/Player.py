#from pygame.sprite import _Group
from abc import ABC, abstractmethod
import pygame

class Player(pygame.sprite.Sprite, ABC):

    def __init__(self, spritePNG, strategy, mediator, team):
        super().__init__()
        self.image = pygame.image.load(spritePNG).convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 485, self.image.get_height() - 485))
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect() 
        self.strategy = strategy
        self.mediator = mediator
        self.dx = 0
        self.dy = 0
        self.distance = 0
        self.move_speed = 7
        self.hasBall = False
        self.team = team
        # self.direction_of_movement = ""
            
    @abstractmethod
    def update(self):
        pass

    def animation_of_move(self):
        if self.distance != 0:
            '''
            self.direction_of_movement = ""
            old_x = self.rect.x
            old_y = self.rect.y
            '''
            self.rect.x += self.dx / self.distance * self.move_speed
            self.rect.y += self.dy / self.distance * self.move_speed
            '''
            if self.rect.x > old_x: # avanzo hacia la derecha (Right)
                self.direction_of_movement += "R"
            elif self.rect.x < old_x: # avanzo hacia la izquierda (Left)
                self.direction_of_movement += "L"
          # else:  no hay movimiento en x 
            if self.rect.y > old_y: # avanzo hacia abajo (Bottom)
                self.direction_of_movement += "B"
            elif self.rect.y < old_y: # avanzo hacia arriba (Top)
                self.direction_of_movement += "T"
          # else:  no hay movimiento en y

            # RB | RT | LB | LT = movimientos en diagonal
            '''

    def calculate_new_pos(self, target_x, target_y):
        if (target_x == self.rect.centerx) and (target_y == self.rect.centery):
            return target_x, target_y
        self.dx = target_x - self.rect.centerx
        self.dy = target_y - self.rect.centery
        self.distance = (self.dx ** 2 + self.dy ** 2) ** 0.5

        new_x = (self.rect.x + self.dx / self.distance * self.move_speed)
        new_y = (self.rect.y + self.dy / self.distance * self.move_speed)
        return new_x, new_y

    def setPosition(self, pos):
         self.rect.center = pos
