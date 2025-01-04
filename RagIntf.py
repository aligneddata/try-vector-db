from abc import ABC, abstractmethod

class RagIntf(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate_answer(self, query: str):
        pass
