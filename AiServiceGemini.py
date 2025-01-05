import logging
import os
import time
import google.generativeai as genai  # google-generativeai
from AiServiceIntf import AiServiceIntf

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', 
                    level=os.getenv('DEBUG_LEVEL', 'INFO'))

class AiServiceGemini(AiServiceIntf):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.rate_limit_delay=int(os.getenv("GEMINI_DELAY", "4"))

    def get_response(self, query: str, context: str):
        final_prompt = self.make_rag_prompt(query=query, context=context)
        logging.info("Final Prompt >>>> [\n%s ... \n]" %  (final_prompt[:9999]))
        response = self.model.generate_content(final_prompt)
        output_message = response.text
        logging.info("Response generated from GenAI Service <<<< [%s]" % str(output_message))

        logging.info("Delaying [%d] seconds" % self.rate_limit_delay)
        time.sleep(self.rate_limit_delay)
        return output_message
