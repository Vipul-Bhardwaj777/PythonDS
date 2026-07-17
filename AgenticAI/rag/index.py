"""
Indexing: load nodejs.pdf -> chunks -> embeddings -> Qdrant collection learning_rag.

Prereqs: Qdrant running (see rag/docker-compose.yml), OPENAI_API_KEY in AgenticAI/.env.

From AgenticAI:
  cd rag
  docker compose up -d
  cd ..
  python rag/index.py

Run once, or again after changing the PDF / wiping Qdrant.
"""

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

# Indexing Phase

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

# Load Pdf
pdf_loader = PyPDFLoader(pdf_path)
docs = pdf_loader.load()

# Chunking
pdf_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
chunks = pdf_splitter.split_documents(documents=docs)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)
