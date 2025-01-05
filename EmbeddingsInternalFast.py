import os
import logging
import requests
import json
from EmbeddingsIntf import EmbeddingsIntf

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'DEBUG'))


class EmbeddingsInternalFast(EmbeddingsIntf):
    def __init__(self, chunk_size: int, dimension: int):
        super().__init__(chunk_size, dimension)
        self.MODEL = "nomic-embed-text:latest"
        self.EMBED_API = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api") + "/embeddings"
        
    def encode(self, text: str):
        logging.debug("Embedding req >>>>>> [%s]" % text[0:self.CHUNK_SIZE])
        data = {}
        data["model"] = self.MODEL
        data["prompt"] = text
        result = self._post_json(self.EMBED_API, data)
        logging.debug("Embedded resp <<<<<< %s " % result)
        return result['embedding']

    def decode(self, embeddings):
        pass

    def _post_json(self, url, dict_data):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, data=json.dumps(dict_data), headers=headers, verify=False)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.RequestException as e:
            logging.error(f"Exception raised: {e}; " + response.text)
            return False