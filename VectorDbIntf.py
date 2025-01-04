from abc import ABC, abstractmethod
from SplitterIntf import SplitterIntf
from EmbeddingsIntf import EmbeddingsIntf

class VectorDbIntf(ABC):
    @abstractmethod
    def __init__(self, token_limit: int, dimension: int, splitter: SplitterIntf, embedder: EmbeddingsIntf):
        super().__init__()
        self.TOKEN_LIMT = token_limit
        self.DIM = dimension
        self.splitter: SplitterIntf = splitter
        self.embedder: EmbeddingsIntf = embedder
        
    @abstractmethod
    def create_or_get_index(self, index_name: str):
        pass

    @abstractmethod
    def load_from_file(self, index_name: str, filename: str):
        pass
    
    @abstractmethod
    def load_from_texts(self, index_name: str, list_of_texts):
        pass
    
    @abstractmethod
    def similarity_search(self, index_name: str, query: str, k=4):
        pass
