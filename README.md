# RAG-Based ToS & Privacy Policy Q&A

This project builds a retrieval-augmented generation (RAG) system to answer plain English questions about Terms of Service and Privacy Policies.

No one reads these documents, but people still care about specific things like data sharing, liability, or account rules. This system retrieves the relevant clauses and answers questions directly from them instead of guessing.

---

## What it does

- Scrapes Terms of Service and Privacy Policies from major platforms  
- Cleans and stores them as a text corpus with metadata  
- Splits documents into chunks and indexes them in a vector database  
- Retrieves relevant clauses for a given question  
- Uses an LLM to generate grounded answers from those clauses  

---

## Pipeline

### 1. Data collection
- Scraping using requests + BeautifulSoup  
- Playwright fallback for JS-heavy pages  

### 2. Cleaning
- Removes boilerplate like headers, scripts, navigation  

### 3. Chunking
- Recursive chunking (2048 chars, overlap)  
- Also tested smaller chunks and sentence-level chunks  

### 4. Indexing
- Embeddings with OpenAI `text-embedding-3-small`  
- Stored in ChromaDB  

### 5. Retrieval + QA
- Top-k semantic retrieval (k = 3)  
- Context passed to GPT-4o-mini for answer generation  

---

## Evaluation

- 51 question-answer pairs across real policies  
- Compared:
  - Semantic retrieval  
  - BM25 keyword search  
  - No-retrieval baseline  

### Metrics
- Embedding similarity  
- Fuzzy match  
- LLM-as-a-judge  

**Key result:**  
RAG significantly outperforms the baseline, especially on factual questions where the baseline tends to hallucinate.

---

## Main takeaway

Retrieval matters.

Grounding the model in actual policy text leads to more accurate and reliable answers, especially for specific details like numbers, limits, and legal conditions.

---

## Limitations

- Struggles with questions that require combining multiple clauses  
- Fixed k for retrieval  
- No negative examples in evaluation  

---

## Future work

- Fine-tune a model on ToS;DR summaries  
- Try HyDE for better retrieval  
- Improve multi-clause reasoning  

---

## Stack

- Python  
- LangChain  
- ChromaDB  
- OpenAI API  
- Playwright / BeautifulSoup  
