import logging
import os
import unittest
import Tools
from AiServiceIntf import AiServiceIntf

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'INFO'))


class AiServiceIntSmall(AiServiceIntf):
    def __init__(self):
        self.MODEL = "llama3.2:1b"
        #self.MODEL = "smollm2:360m"
        self.GEN_API = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api") + "/generate"

    def get_response(self, query: str, context: str):
        final_prompt = self.make_rag_prompt(query=query, context=context)
        logging.debug("Final Prompt >>>> [\n%s ... \n]" %  (final_prompt[:9999]))
        data = {}
        data["model"] = self.MODEL
        data["prompt"] = final_prompt
        data["stream"] = False
        result = Tools.post_json(self.GEN_API, data)
        logging.debug("Response generated from GenAI Service <<<< [%s]" % str(result))
        return result['response']


class TestAiServiceIntSmall(unittest.TestCase):
    def test_1(self):
        llm = AiServiceIntSmall()
        print(llm.get_response("How big is Amazon?", "Amazon is a tropic region in South America."))
    
    def test_2(self):
        llm = AiServiceIntSmall()
        print(llm.get_response("How big is Amazon?", "Amazon is an American company."))    