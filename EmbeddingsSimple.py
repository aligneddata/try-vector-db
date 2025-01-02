from abc import ABC, abstractmethod
import AppSettings
import unittest

class EmbeddingsSimple(ABC):
    def __init__(self):
        super().__init__()
        
    def encode(self, text: str, dim: int):
        embeddings = [ord(c) for c in text]
        for i in range(len(embeddings), dim):
            embeddings.append(0)
        return embeddings

    def decode(self, embeddings):
        return [chr(i) for i in embeddings]
        

class TestEmbeddingsSimple(unittest.TestCase):
    def setUp(self):
        self.embd = EmbeddingsSimple()
        self.test_str = 'abcd1234'
        self.test_embds = [97, 98, 99, 100, 49, 50, 51, 52]
        self.dim = AppSettings.EMBEDDINGS_DIM
        
    def test_1_enc(self):
        print(self.embd.encode(self.test_str, self.dim))

    def test_2_dec(self):
        print(self.embd.decode(self.test_embds))