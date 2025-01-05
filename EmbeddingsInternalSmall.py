import os
import logging
import requests
import json
from EmbeddingsIntf import EmbeddingsIntf
import Tools

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'DEBUG'))


class EmbeddingsInternalSmall(EmbeddingsIntf):
    def __init__(self, chunk_size: int, dimension: int):
        super().__init__(chunk_size, dimension)
        self.MODEL = "nomic-embed-text:latest"
        self.EMBED_API = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api") + "/embeddings"
        
    def encode(self, text: str):
        logging.debug("Embedding req >>>>>> [%s]" % text[0:self.CHUNK_SIZE])
        data = {}
        data["model"] = self.MODEL
        data["prompt"] = text
        result = Tools.post_json(self.EMBED_API, data)
        logging.debug("Embedded resp <<<<<< %s " % result)
        return result['embedding']

    def decode(self, embeddings):
        pass
