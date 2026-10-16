"""
Day 3 - Basic RAG, Step 1: Ingest a document

Loads a PDF, cuts it into small chunks, turns each chunk into an
embedding (numbers that capture its meaning), and stores all of
that in a local, searchable vector database (Chroma).

Run it:
    python ingest.py your_file.pdf
"""

import os
import sys

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()


def main(pdf_path: str) -> None:
    # 1. DOCUMENT LOADER - opens the PDF file and pulls out its raw text,
    #    one "document" per page.
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} page(s) from {pdf_path}")

    # 2. TEXT SPLITTER - cuts the long text into small, overlapping
    #    chunks (500 characters each, overlapping by 50) so the AI can
    #    search and read them properly later. The overlap stops a
    #    sentence from being awkwardly cut in half between two chunks.
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunk(s)")

    # 3. EMBEDDINGS - turns each chunk's text into a list of numbers
    #    that captures its meaning. Chunks with similar meaning end up
    #    with similar numbers.
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    # 4. VECTOR STORE - a searchable database of those numbers. We save
    #    it to a local folder called "db" so ask.py can reopen it later
    #    without re-processing the PDF every time.
    Chroma.from_documents(chunks, embeddings, persist_directory="db")
    print("Saved to local vector store: ./db")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py your_file.pdf")
        sys.exit(1)
    main(sys.argv[1])
