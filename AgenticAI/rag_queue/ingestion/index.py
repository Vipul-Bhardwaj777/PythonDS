"""Embed data/nodejs.pdf into the Qdrant collection `nodejs_docs`."""

from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

pdf_path = Path(__file__).resolve().parent.parent / "data" / "usda_nutrition.pdf"

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
    collection_name="usda_nutrition",
)
