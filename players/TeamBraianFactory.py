from Strategies.braianStrategy import BraianStrategy
from players.goalKeeper import GoalKeeper
from players.playerField import PlayerField
from players.teamFactory import TeamFactory

class TeamBraianFactory(TeamFactory):

    def __init__(self, spritePNG, mediator, team, cantPlayers):
        super().__init__(spritePNG, mediator, team, cantPlayers)

    def createTeam(self):
        players = set()
        strategy = BraianStrategy()
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
