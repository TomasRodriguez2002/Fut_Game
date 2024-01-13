from abc import ABC, abstractmethod
import pygame

class Strategy(ABC):

    def __init__(self):
        self.mediator = None
        self.player = None

    def setMediator(self, mediator):
        self.mediator = mediator

    def setPlayer(self, player):
        self.player = player

    @abstractmethod
    def getProxPos(self):
        pass

    @abstractmethod
    def with_ball(self):
        pass

    @abstractmethod
    def where_to_pass(self):
        pass