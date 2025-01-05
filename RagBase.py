import unittest
from abc import ABC, abstractmethod
from RagIntf import RagIntf
from VectorDbPgvector import VectorDbPgvector
from SplitterIntf import SplitterIntf
from SplitterSimple import SplitterSimple
from EmbeddingsIntf import EmbeddingsIntf
from EmbeddingsGemini import EmbeddingsGemini
from AiServiceIntf import AiServiceIntf
from AiServiceGemini import AiServiceGemini

class RagBase(RagIntf):
    def __init__(self):
        pass
        
    def generate_answer(self, query: str):
        related_texts = self.vector_store.similarity_search(self.INDEX_NAME, query=query, k=1)
        context = ''
        for text in related_texts:
            context += "\n\n" + text
        answer = self.gen_ai.get_response(query, context)
        return answer
    
    def load_file(self, filename):
        self.vector_store.load_from_file(self.INDEX_NAME, filename)

    def close(self):
        self.vector_store.close()

