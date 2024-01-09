from abc import ABC, abstractmethod

class IPlayerField(ABC):

    @abstractmethod
    def update(self):
        pass