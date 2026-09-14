# RAG Project

## What it does

This project is a simple RAG application.

It uses Python documents as data. The documents are split into small parts and stored in PostgreSQL with pgvector.

When the user asks a question, the application finds the most relevant parts and uses them to generate an answer with an LLM.

## Technologies

* Python
* PostgreSQL
* pgvector
* Sentence Transformers
* Ollama
* Docker

## How it works

```text
Documents
   ↓
Chunks
   ↓
Embeddings
   ↓
PostgreSQL
   ↓
Question
   ↓
Top-3 results
   ↓
LLM
   ↓
Answer


## Files

documents/
    pandas.txt
    python.txt
    spark.txt

ingestion.py
rag.py
requirements.txt


## How to run

Install the packages:

pip install -r requirements.txt

Run:

python rag.py


Then write a question.

Example:

What is Spark?


The application finds related information from the documents and gives an answer.

## Architecture

```text
Documents
   ↓
Chunks
   ↓
Embeddings
   ↓
PostgreSQL + pgvector
   ↓
Question
   ↓
Top-3 relevant chunks
   ↓
Ollama
   ↓
Answer