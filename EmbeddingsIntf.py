from abc import ABC, abstractmethod

class EmbeddingsIntf(ABC):
    @abstractmethod
    def __init__(self, token_limit: int, dimension: int):
        super().__init__()
        self.TOKEN_LIMIT = token_limit
        self.DIM = dimension
        
    @abstractmethod
    def encode(self, text: str):
        pass

    @abstractmethod
    def decode(self, embeddings):
        pass
