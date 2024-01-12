from abc import ABC, abstractmethod
import pygame

class Strategy(ABC, pygame.sprite.Sprite):

    def __init__(self):
        pass

    @abstractmethod
    def getProxPos(self,player,mediator):
        pass

    @abstractmethod
    def with_ball(self,player,mediator):
        pass

    @abstractmethod
    def where_to_pass(self,player,mediator):
        pass