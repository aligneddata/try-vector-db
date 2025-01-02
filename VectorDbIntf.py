from abc import ABC, abstractmethod

class VectorDbIntf(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def create_or_get_index(self, index_name: str, dimension: int):
        pass

    @abstractmethod
    def load_from_file(self, index_name: str, filename: str):
        pass
    
    @abstractmethod
    def load_from_texts(self, index_name: str, list_of_texts):
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, k=4):
        pass
