# For creating text embeddings
from sentence_transformers import SentenceTransformer

# For PostgreSQL
import psycopg2

# For pgvector
from pgvector.psycopg2 import register_vector

# For the LLM
import ollama

# For environment variables
from dotenv import load_dotenv
import os

load_dotenv()

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
except Exception as e:
    print("Database connection error:", e)
    exit()

# Enable pgvector
register_vector(conn)

# Create a cursor
cur = conn.cursor()

# Get user question
query = input("Ask a question: ")

# Create query embedding
query_embedding = model.encode(query)

# Search for the most similar chunks
try:
    cur.execute(
        """
        SELECT id, content
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT 3
        """,
        (query_embedding,)
    )
except Exception as e:
    print("Retrieval error:", e)
    conn.close()
    exit()

# Get the results
results = cur.fetchall()

# Create the context
context = "\n\n".join(result[1] for result in results)

# Create the prompt
prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{query}
"""

# Generate the answer
try:
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
except Exception as e:
    print("LLM error:", e)
    conn.close()
    exit()

# Show the answer
print(response["message"]["content"])
