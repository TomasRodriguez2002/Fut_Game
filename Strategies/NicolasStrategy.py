from Strategies.Strategy import Strategy
import random

from players.GoalKeeper import GoalKeeper
from Constantes import *

class NicolasStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def getProxPos(self):
        # return self.mediator.prueba()
        if isinstance(self.player, GoalKeeper):
            if self.player.team == True:
                random_x = random.randint(0, 500)
                random_y = random.randint(0,500)
                return random_x, random_y
            else:
                random_x = random.randint(0,500)
                random_y = random.randint(0,500)
                return random_x, random_y
        else:
            return self.mediator.prueba()

    def with_ball(self):
        return 2

    def where_to_pass(self, player, mediator):
        random_x = random.randint(0, 1000)
        random_y = random.randint(0, 1000)
        return random_x, random_y
