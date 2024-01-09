from abc import ABC, abstractmethod

class IPlayerFactory(ABC):

    @abstractmethod
    def createPlayer():
        pass