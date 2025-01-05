from abc import ABC, abstractmethod


class AiServiceIntf(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_response(self, prompt_message: str, context: str):
        pass

    def make_rag_prompt(self, query, context) -> str:
        prompt = ("""
            You are a helpful chatbot that answers QUESTION by referencing CONTEXT included below. 
            Your answers are complete, comprehensive, and include all relevant background information. 
            You answers are in a friendly tone.  
            You don't ask questions back. If you don't know the answer, just say 'I do not know'. 
            QUESTION: '{query}'
            CONTEXT: '{context}'

            YOURS ANSWERS:
        """).format(query=query, context=context)
        return prompt

