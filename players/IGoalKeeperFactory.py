from abc import ABC, abstractmethod

class IGoalKeeperFactory(ABC):

    @abstractmethod
    def createGoalKeeper(self): 
        pass