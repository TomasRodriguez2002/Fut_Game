from abc import ABC, abstractmethod

class Strategy(ABC):

    def __init__(self):
        self.mediator = None

    def setMediator(self, mediator):
        self.mediator = mediator

    @abstractmethod
    def getProxPos(self, player):
        pass

    @abstractmethod
    def with_ball(self, player):
        pass

    @abstractmethod
    def where_to_pass(self, player):
        pass