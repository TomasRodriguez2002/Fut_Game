from Strategies.NicolasStrategy import NicolasStrategy
from players.GoalKeeper import GoalKeeper
from players.PlayerField import PlayerField
from players.TeamFactory import TeamFactory


class TeamNicolasFactory(TeamFactory):

    def __init__(self, spritePNG, mediator, team, cantPlayers):
        super().__init__(spritePNG, mediator, team, cantPlayers)

    def createTeam(self):
        players = set()
        # creacion de jugadores de campo
        for i in range(self.cantPlayers-1):
            strategy = NicolasStrategy()
            player = PlayerField(self.spritePNG, strategy, self.mediator, self.team) 
            strategy.setMediator(self.mediator)
            strategy.setPlayer(player)
            players.add(player)
        # creacion de arquero
        strategy = NicolasStrategy()
        player = GoalKeeper(self.spritePNG, strategy, self.mediator, self.team)
        strategy.setMediator(self.mediator)
        strategy.setPlayer(player)
        players.add(player)
        return players
