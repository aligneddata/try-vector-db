# try-vector-db
* Purpose: implement the basics of a RAG system. 
* Side research goal(s):
  - Is it feasible to run a RAG system completely internally (behind a firewall)
  - Create a few reusable classes to manage key components of a RAG system

# How to run
## Main programs
<pre>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_py3.9.2.txt
#create postgres/pgvector system 
#use the templates in docs folder to establish a ~/.try-vector-db.env.sh file
#register a gemini account and get key
bash run.sh
</pre>
## Additional: using Pinecone via Langchain
<pre>
#After all above steps, register a Pinecone and get key
python load_data.py
python query.py
</pre>

# Design and Implementation
## Rag Ext Free (Gemini)
* Encoder: Gemini
* Vector store: pgvector
* LLM:
  - Gemini: took 1 second to return, in great quality consistently.

## Rag Int Small
* Encoder: 
  - nomic-embed-text:latest. Usually took less than 1 second turnover.
  - bge-m3:latest: Much heavier in memory use than nomic (give up).
* Vector store: pgvector
* LLM via Ollama: 
  - qwen:0.5b missed the question consistently
  - llama3.2:1b very good. Took 1'5" to load. Mostly great response quality. Sometimes missed the question. Stick to this choice.
  - smollm:1.7b works very well. Took 2'10" to load.
  - smollm:360m partially missed the questions. Took 2'40" to load.

## RegOptim (Tentative concluded best choice)
* Use nomic-embed-text:latest and host it internally.
* Keep data internally in Pgvector
* For LLM, use Gemini Flash 1.5 when it is still free (5 requests / minute)

# Some thoughts
* Encoder can be hosted internally. Outsource may be expensive.
* Vector store has a lot of data and will grow much larger in future. It may be too expensive to outsource.
* Internally hosted LLM is hard to match the same production performance and quality as an external API service from a cloud  AI provider.
* Some parameters must be planned carefully ahead. Or else, it is expensive to re-index all data.
  - Chunk size stored and to be sent to LLM
  - Token limit for a encoder and LLM input window limit
  - Index dimension stored (encoder's output)
* Perhaps the most important decision is to choose a high-quality, high-performance, and long-term supported encoder. 

# Next Experiments / Future Road Maps
* Explore advanced RAG techniques. Refernce and thanks: https://medium.com/@saurabhgssingh/why-your-rag-is-not-working-96053b4d5305
  - Enrich query by sending the query to LLM first
    - <pre>
      prompt ="""You are a helpful expert financial research assistant. Your users are asking questions about an annual report. \
        Suggest up to five additional related questions to help them find the information they need, for the provided question. \
        Suggest only short questions without compound sentences. Suggest a variety of questions that cover different aspects of the topic.\
        Make sure they are complete questions, and that they are related to the original question.\
        Output one question per line. Do not number the questions.
        Query: {query}"""
      query = "What were the most important factors that contributed to increases in revenue?"
      </pre>
  - Re-rank search results:
   - <pre>
      from typing import List
      from sentence_transformers import CrossEncoder
      cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
      def rank_documents(cross_encoder:CrossEncoder,query:str,retrieved_documents:List[str]):
          """
          Ranks retrieved documents based on their relevance to a given query using a cross-encoder model.

          Parameters:
          - cross_encoder (CrossEncoder): A cross-encoder model from the sentence-transformers library.
          - query (str): The query string for which the documents are to be ranked.
          - retrieved_documents (List[str]): A list of document strings that have been retrieved as potentially relevant to the query.

          Returns:
          - dict: A dictionary where the key is the rank position (starting from 0 for the most relevant document)
            and the value is the document string. The documents are ranked in descending order of relevance to the query.

          Usage:
          ranked_docs = rank_documents(cross_encoder, query, retrieved_documents)

          Note: This function requires the sentence-transformers library and a pretrained cross-encoder model.
          """
          pairs = [[query, doc] for doc in retrieved_documents]
          scores = cross_encoder.predict(pairs)
          ranks = np.argsort(scores)[::-1]
          ranked_docs = {rank_num:doc for rank_num,doc in zip(ranks,retrieved_documents)}
          return ranked_docs

      #usage
      ranked_docs= rank_documents(cross_encoder,query,retrieved_documents)
    </pre>
  - Others: embedding adaptors, fine tuning the embedding models, and deep chunking approaches (what are they?)
* Try using sparse vectors than dense vectors and see its effectiveness.
* Try using 'pgai vectorizer', a (trigger+queue+worker) solution that works behind a normal pg table to manage vectors.
  - https://www.youtube.com/watch?v=3GPLb12FfNw
  - Try using 'ai', an extension to Postgres that is supposed to simplify the use of pgvector.

# CHANGE LOGS
* 2025.1.5 Wrap up: Added LICENSE; updated README.
* 2025.1.4 Tested the quality of internally hosted llm.
* 2025.1.3 Get coarse Rag/Ai/Embed/Vecdb interfaces working.

# Contacts
* This repo has been wrapped up as Jan 5, 2025. It will not be actively maintained. However, your comments/PRs are welcome and will be responsed whenever I'm available.
* Contact: AlignedData@gmail.com