from Strategies.GonzaloStrategy import GonzaloStrategy
from players.GoalKeeper import GoalKeeper
from players.PlayerField import PlayerField
from players.TeamFactory import TeamFactory

class TeamGonzaloFactory(TeamFactory):

    def __init__(self, spritePNG, mediator, team, cantPlayers):
        super().__init__(spritePNG, mediator, team, cantPlayers)

    def createTeam(self):
        players = set()
        strategy = GonzaloStrategy()
        strategy.setMediator(self.mediator)
        player = None
        # creacion de jugadores de campo
        for i in range(self.cantPlayers - 1):
            player = PlayerField(self.spritePNG, strategy, self.mediator, self.team)
            players.add(player)
        # creacion de arquero
        player = GoalKeeper(self.spritePNG, strategy, self.mediator, self.team)
        players.add(player)
        return players