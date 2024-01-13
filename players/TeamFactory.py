from abc import ABC, abstractmethod

class TeamFactory(ABC):

    def __init__(self, spritePNG, mediator, team, cantPlayers):
        self.spritePNG=spritePNG
        self.mediator=mediator
        self.team=team
        self.cantPlayer=cantPlayers

    @abstractmethod
    def createTeam(self):
        pass