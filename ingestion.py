# For creating text embeddings
from sentence_transformers import SentenceTransformer

# For PostgreSQL
import psycopg2

# For pgvector
from pgvector.psycopg2 import register_vector

# For reading files
import os

# For environment variables
from dotenv import load_dotenv

load_dotenv()

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Get all text files
files = os.listdir("documents")

# Store documents
documents = []

# Read all text files
for filename in files:
    if filename.endswith(".txt"):
        with open(f"documents/{filename}", "r", encoding="utf-8") as file:
            documents.append(file.read())

# Split documents into chunks
chunks = []

for document in documents:
    chunks.extend(document.strip().split("\n\n"))

# Create embeddings
chunk_embeddings = model.encode(chunks)

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

# Insert chunks and embeddings
for chunk, embedding in zip(chunks, chunk_embeddings):
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (chunk, embedding)
    )

# Save changes
conn.commit()
