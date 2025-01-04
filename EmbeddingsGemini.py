from abc import ABC, abstractmethod
import google.generativeai as genai
import os
from EmbeddingsIntf import EmbeddingsIntf
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'DEBUG'))


class EmbeddingsGemini(EmbeddingsIntf):
    def __init__(self, token_limit: int, dimension: int):
        super().__init__(token_limit, dimension)
        self.MODEL = "models/text-embedding-004"
        
    def encode(self, text: str):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        logging.debug("Embedding req >>>>>> [%s]" % text[0:self.TOKEN_LIMIT])
        result = genai.embed_content(
                model=self.MODEL,
                content=text[0:self.TOKEN_LIMIT])
        logging.debug("Embedded resp <<<<<< %s " % result)
        return result['embedding']

    def decode(self, embeddings):
        pass
