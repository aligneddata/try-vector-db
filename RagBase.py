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
        self.INDEX_NAME = "rag_base"
        self.CHUNK_SIZE = 2048
        self.DIM = 768
        self.splitter: SplitterIntf = SplitterSimple()
        self.embeder: EmbeddingsIntf = EmbeddingsGemini(self.CHUNK_SIZE, self.DIM)
        
        self.vector_store = VectorDbPgvector(self.CHUNK_SIZE, self.DIM, self.splitter, self.embeder)
        self.vector_store.create_or_get_index(self.INDEX_NAME, self.DIM)
        
        self.gen_ai: AiServiceIntf = AiServiceGemini()
        
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

