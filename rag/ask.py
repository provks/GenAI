"""
Day 3 - Basic RAG, Step 2: Ask questions about your document

Loads the vector store built by ingest.py, finds the chunks most
relevant to your question, and asks the AI to answer using ONLY
those chunks. If the answer isn't in the document, it must say
"not in my documents" instead of guessing.

Run it (after running ingest.py first):
    python ask.py
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Re-open the same local vector store that ingest.py already filled.
vector_store = Chroma(persist_directory="db", embedding_function=embeddings)

# RETRIEVER - searches the vector store and returns the 3 chunks
# that are most similar (most relevant) to whatever question it gets.
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# PROMPT TEMPLATE - this is what makes the answer "grounded": it tells
# the AI to use ONLY the retrieved context, and gives the exact wording
# to use when the answer isn't there.
prompt = ChatPromptTemplate.from_template(
    """Answer the question using ONLY the context below. Do not use any
outside knowledge. If the answer is not in the context, reply with
exactly: "not in my documents"

Context:
{context}

Question: {question}
"""
)

parser = StrOutputParser()


def format_chunks(chunks) -> str:
    # The retriever gives us a list of chunk objects; this joins their
    # text together into one block to drop into the prompt's {context}.
    return "\n\n".join(chunk.page_content for chunk in chunks)


# THE RAG CHAIN (LCEL):
#   - "context": the question goes through the retriever, then the
#     results are formatted into plain text
#   - "question": passed through unchanged (RunnablePassthrough)
#   - both get filled into the prompt, sent to the model, then the
#     reply is cleaned up by the parser
rag_chain = (
    {"context": retriever | format_chunks, "question": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

if __name__ == "__main__":
    print("Chat With Your PDF - ask a question, or 'quit' to stop")
    while True:
        question = input("\n> ").strip()
        if question.lower() == "quit":
            break
        if not question:
            continue
        print(rag_chain.invoke(question))
