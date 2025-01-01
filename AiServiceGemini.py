import logging
import os
import time
import google.generativeai as genai  # google-generativeai
from AiServiceIntf import AiServiceIntf

class AiServiceGemini(AiServiceIntf):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.rate_limit_delay=int(os.getenv("GEMINI_DELAY", "4"))

    def get_response(self, query: str, context: str):
        final_prompt = "You are an accounting book keeper, processing an textual invoice." + \
                "Answer this question: " + query + \
                "According to this context information: " + context
        logging.info("Message to ask AI Service >>>> [\n%s ... \n]" %  (final_prompt[:4096]))
        response = self.model.generate_content(final_prompt)
        output_message = response.text
        logging.info("Response returned from AI Service <<<< [%s]" % str(output_message))

        logging.info("Delaying [%d] seconds" % self.rate_limit_delay)
        time.sleep(self.rate_limit_delay)
        return output_message #.replace('```json', '').replace('```','')
