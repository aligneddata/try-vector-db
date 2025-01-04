from abc import ABC, abstractmethod


class AiServiceIntf(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, prompt_message: str, context: str):
        pass

    @abstractmethod
    def make_rag_prompt(query, relevant_passage) -> str:
        pass
