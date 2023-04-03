from abc import ABC, abstractmethod

class Binder(ABC):
    
        @abstractmethod
        def send(self, scopes):
            pass