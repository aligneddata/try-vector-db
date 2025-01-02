from abc import ABC, abstractmethod

class SplitterIntf(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def split(self, text: str, chunk_size: int):
        pass
