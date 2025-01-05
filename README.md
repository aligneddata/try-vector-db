# try-vector-db

## Rag Ext Free (Gemini)
* Encoder: Gemini
* Vector store: pgvector
* LLM:
  - Gemini: took 1 second to return, in great quality consistently.

## Rag Int Small
* Encoder: 
  - nomic-embed-text:latest. Usually took less than 1 second turnover.
  - bge-m3:latest: Took a minute for the inital load.
* Vector store: pgvector
* LLM via Ollama: 
  - qwen:0.5b missed the question consistently
  - llama3.2:1b very good. Took 1'5". Most time great. Sometimes missed the question.
  - smollm:1.7b works very well. Took 2'10".
  - smollm:360m partially missed the questions. Took 2'40".


# Some thoughts
* Encoder can be hosted internally. Outsource may be expensive.
* Vectorstore has a lot of data and will have a lot in future. It may be too expensive to outsource.
* Internally hosted LLM is hard to achieve production quality as good as a cloud service.
* Some parameters must be planned carefully ahead. Or else, it is expensive to re-index all data.
  - Chunk size stored and to be sent to LLM
  - Token limit for a encoder and LLM input
  - Index dimension stored (encoder's output)
* Perhaps the most important decision is to choose a high-quality, high-performance, and long-term supported encoder. 

# Tentative Conclusion
* Use nomic-embed-text:latest
* Keep data internally in Pgvector
* For LLM, use Gemini Flash 1.5 when it is still free (5 req / minute)

# CHANGE LOGS
* 2025.1.4 Tested the quality of internally hosted llm.
* 2025.1.3 Get coarse Rag/Ai/Embed/Vecdb interfaces working.