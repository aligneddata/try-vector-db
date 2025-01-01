from abc import ABC, abstractmethod

class VectorDbIntf(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        
