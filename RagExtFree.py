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

class RagExtFree(RagIntf):
    def __init__(self):
        self.INDEX_NAME = "rag_ext_free"
        self.TOKEN_LIMIT = 2048
        self.DIM = 768
        self.splitter: SplitterIntf = SplitterSimple()
        self.embeder: EmbeddingsIntf = EmbeddingsGemini(self.TOKEN_LIMIT, self.DIM)
        
        self.vector_store = VectorDbPgvector(self.TOKEN_LIMIT, self.DIM, self.splitter, self.embeder)
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


class TestRagExtFree(unittest.TestCase):
    def setUp(self):
        self.rag = RagExtFree()
        self.rag.load_file("z1.txt")

    def tearDown(self):
        self.rag.close()
    
    def test_1_conn(self):
        self.rag.generate_answer("What flight can fly me from Vancouver to Seoul?")
        
    def test_2_conn(self):
        self.rag.generate_answer("How much does it cost to fly from Vancouver to Seoul?")