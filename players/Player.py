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
            
    @abstractmethod
    def update(self):
        pass

    def animation_of_move(self):
        #if self.move_speed != 0 and self.distance != 0:
        self.rect.x += self.dx / self.distance * self.move_speed
        self.rect.y += self.dy / self.distance * self.move_speed
            #self.move_speed -= 1    
        
        #if self.move_speed <= 0:    
        #    self.move_speed = 35
        #    self.is_moving = False

    def calculate_new_pos(self, target_x, target_y):
            self.dx = target_x - self.rect.centerx
            self.dy = target_y - self.rect.centery
            self.distance = (self.dx ** 2 + self.dy ** 2) ** 0.5

            new_x = (self.rect.x + self.dx / self.distance * self.move_speed)
            new_y = (self.rect.y + self.dy / self.distance * self.move_speed)
            return new_x, new_y

    def setPosition(self, pos):
         self.rect.center = pos
