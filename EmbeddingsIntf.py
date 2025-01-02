from abc import ABC, abstractmethod

class EmbeddingsIntf(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def encode(self, text: str):
        pass

    @abstractmethod
    def decode(self, embeddings):
        pass
