from abc import ABC, abstractmethod

class IGoalKeeper(ABC):

    @abstractmethod
    def update(self):
        pass