import os
import sys
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from VectorDbPinecone import VectorDbPinecone


def load_from_file(vectorstore, filename):  
    loader = TextLoader(filename)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    vectorstore.add_documents(docs)

def load_from_text(vectorstore, list_of_texts):
    vectorstore.add_texts(list_of_texts)

index_name = "test"
DIM = 1536 # OpenAI

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

vdb = VectorDbPinecone(index_name, DIM)

vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
load_from_file(vectorstore=vectorstore, filename='test.pdf.txt')
load_from_file(vectorstore=vectorstore, filename='z1.txt')
load_from_text(vectorstore=vectorstore, list_of_texts=['text para 1', 'text para 2'])


