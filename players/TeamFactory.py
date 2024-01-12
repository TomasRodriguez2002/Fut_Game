from abc import ABC, abstractmethod

class TeamFactory(ABC):

    @abstractmethod
    def createTeam(self, spritePNG, mediator, team, cantPlayers):
        pass