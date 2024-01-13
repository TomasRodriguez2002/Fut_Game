from players.TeamFactory import TeamFactory 
from Strategies.NicolasStrategy import NicolasStrategy
from players.PlayerField import PlayerField
from players.GoalKeeper import GoalKeeper

class TeamNicolasFactory(TeamFactory):
    
    def __init__(self, spritePNG, mediator, team, cantPlayers):
        super().__init__(spritePNG, mediator, team, cantPlayers)

    def createPlayer(self):
        players = []
        strategy = None
        player = None
        # creacion de jugadores de campo
        for i in range(super.cantPlayers-1):
            strategy = NicolasStrategy()
            player = PlayerField(super.spritePNG, strategy, super.mediator, super.team) 
            strategy.setMediator(super.mediator)
            strategy.setPlayer(player)
            players.add(player)
        # creacion de arquero
        strategy = NicolasStrategy()
        player = GoalKeeper(super.spritePNG, strategy, super.mediator, super.team)
        strategy.setMediator(super.mediator)
        strategy.setPlayer(player)
        players.add(player)
        return players
