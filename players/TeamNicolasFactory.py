from players.TeamFactory import TeamFactory 
from Strategies import *
from players.PlayerField import PlayerField
from players.GoalKeeper import GoalKeeper

class TeamNicolasFactory(TeamFactory):
    def __init__(self,spritePNG, mediator, team, cantPlayers):
        super().__init__()
        self.spritePNG=spritePNG
        self.mediator=mediator
        self.team=team
        self.cantPlayer=cantPlayers

    def createPlayer(self, spritePNG, mediator, team, cantPlayers):
        team = []
        strategy = None
        player = None
        # creacion de jugadores de campo
        for i in range(cantPlayers-1):
            strategy = NicolasStrategy()
            player = PlayerField(spritePNG, strategy, mediator, team) 
            strategy.setMediator(mediator)
            strategy.setPlayer(player)
            team.add(player)
        # creacion de arquero
        strategy = NicolasStrategy()
        player = GoalKeeper(spritePNG, strategy, mediator, team)
        strategy.setMediator(mediator)
        strategy.setPlayer(player)
        team.add(player)
        return team
