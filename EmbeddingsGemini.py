from abc import ABC, abstractmethod
import google.generativeai as genai
import os
from EmbeddingsIntf import EmbeddingsIntf
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'DEBUG'))


class EmbeddingsGemini(EmbeddingsIntf):
    def __init__(self, chunk_size: int):
        super().__init__(chunk_size)
        self.MODEL = "models/text-embedding-004"
        self.DIM = 768
        
    def encode(self, text: str):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        logging.debug("Embedding req >>>>>> [%s]" % text[0:self.CHUNK_SIZE])
        result = genai.embed_content(
                model=self.MODEL,
                content=text[0:self.CHUNK_SIZE])
        logging.debug("Embedded resp <<<<<< %s " % result)
        return result['embedding']

    def decode(self, embeddings):
        pass
