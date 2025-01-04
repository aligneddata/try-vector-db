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

results = vectorstore.similarity_search(query, k=1)

from AiServiceGemini import AiServiceGemini
ai_service = AiServiceGemini()
for result in results:
    answer = ai_service.get_response(query, result.page_content)
    