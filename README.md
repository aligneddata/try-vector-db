# try-vector-db

## Rag Ext Free (Gemini)
* Encoder: Gemini
* Vector store: pgvector
* LLM:
  - Gemini: took 1 second to return, in great quality consistently.

## Rag Int Small
* Encoder: Gemini
* Vector store: pgvector
* LLM via Ollama: 
  - qwen:0.5b missed the question consistently
  - llama3.2:1b very good. Took 1'5". Most time great. Sometimes missed the question.
  - smollm:1.7b works very well. Took 2'10".
  - smollm:360m partially missed the questions. Took 2'40".

# CHANGE LOGS
* 2025.1.3 Get coarse Rag/Ai/Embed/Vecdb interfaces working.