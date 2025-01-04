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

    def make_rag_prompt(self, query, context):
        prompt = ("""
            You are a helpful and informative bot that answers questions using context from the reference passage included below. \
            Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
            However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
            strike a friendly and converstional tone. \
            If you don't know the answer, just say 'I do not know'. 
            QUESTION: '{query}'
            PASSAGE: '{context}'

            ANSWER:
        """).format(query=query, context=context)
        return prompt
