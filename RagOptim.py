import unittest
from VectorDbPgvector import VectorDbPgvector
from SplitterIntf import SplitterIntf
from SplitterSimple import SplitterSimple
from EmbeddingsIntf import EmbeddingsIntf
from EmbeddingsInternalSmall import EmbeddingsInternalSmall
from AiServiceIntf import AiServiceIntf
from RagBase import RagBase
from AiServiceGemini import AiServiceGemini

# RAG using all internal resources and using slim models
class RagOptim(RagBase):
    def __init__(self):
        self.INDEX_NAME = "rag_optim"
        self.CHUNK_SIZE = 2048
        self.splitter: SplitterIntf = SplitterSimple()
        self.embeder: EmbeddingsIntf = EmbeddingsInternalSmall(self.CHUNK_SIZE)
        
        self.vector_store = VectorDbPgvector(self.CHUNK_SIZE, self.embeder.DIM, self.splitter, self.embeder)
        self.vector_store.create_or_get_index(self.INDEX_NAME, self.embeder.DIM)
        
        self.gen_ai: AiServiceIntf = AiServiceGemini()


class TestRagExtFree(unittest.TestCase):
    def setUp(self):
        self.rag = RagOptim()
        self.rag.load_file("z1.txt")

    def tearDown(self):
        self.rag.close()
    
    def test_1_conn(self):
        self.rag.generate_answer("What flight can fly me from Vancouver to Seoul?")
        
    def test_2_conn(self):
        self.rag.generate_answer("How much does it cost to fly from Vancouver to Seoul?")