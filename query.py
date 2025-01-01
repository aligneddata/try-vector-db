import os
import sys
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import google.generativeai as genai

if len(sys.argv) < 2:
    print("Error: <command> <query>")
    sys.exit(1)

query = sys.argv[1]

index_name = "test"
embeddings = OpenAIEmbeddings()


vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

results = vectorstore.similarity_search(query, k=2)
# Response:
# [
#    Document(page_content='Ketanji Onyika Brown Jackson is an American lawyer and jurist who is an associate justice of the Supreme Court of the United...', metadata={'chunk': 0.0, 'source': 'https://en.wikipedia.org/wiki/Ketanji_Brown_Jackson', 'title': 'Ketanji Brown Jackson', 'wiki-id': '6573'}),  
#    Document(page_content='Jackson was nominated to the Supreme Court by President Joe Biden on February 25, 2022, and confirmed by the U.S. Senate...', metadata={'chunk': 1.0, 'source': 'https://en.wikipedia.org/wiki/Ketanji_Brown_Jackson', 'title': 'Ketanji Brown Jackson', 'wiki-id': '6573'}),  
#    Document(page_content='Jackson grew up in Miami and attended Miami Palmetto Senior High School. She distinguished herself as a champion debater...', metadata={'chunk': 3.0, 'source': 'https://en.wikipedia.org/wiki/Ketanji_Brown_Jackson', 'title': 'Ketanji Brown Jackson', 'wiki-id': '6573'}),
#    Document(page_content='After high school, Jackson matriculated at Harvard University to study government, having applied despite her guidance...', metadata={'chunk': 5.0, 'source': 'https://en.wikipedia.org/wiki/Ketanji_Brown_Jackson', 'title': 'Ketanji Brown Jackson', 'wiki-id': '6573'})
# ]   

from AiServiceGemini import AiServiceGemini
ai_service = AiServiceGemini()
for result in results:
    print('>>>>>', result.page_content)
    answer = ai_service.get_response(query, result.page_content)
    print('Answer <<<<<', answer)
    