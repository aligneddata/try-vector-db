from abc import ABC, abstractmethod

class EmbeddingsIntf(ABC):
    @abstractmethod
    def __init__(self, chunk_size: int, dimension: int):
        super().__init__()
        self.CHUNK_SIZE = chunk_size
        self.DIM = dimension
        
    @abstractmethod
    def encode(self, text: str):
        pass

    @abstractmethod
    def decode(self, embeddings):
        pass
