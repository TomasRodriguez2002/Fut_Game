from Strategies.Strategy import Strategy

class TomasRStrategy(Strategy):
    def __init__(self):
        super().__init__()
       
    def getProxPos(self):
        return self.mediator.prueba()

    def with_ball(self):
        return 1

    def where_to_pass(self):
        pass