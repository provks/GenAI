# Day 3 — LangChain & Basic RAG

Quick, simple notes. Two small projects in this folder: `chain_demo.py` / `chain_with_memory.py` (LangChain basics) and `rag/` (a full RAG app).

## Picture: How It All Fits Together

![LangChain + RAG diagram](images/langchain_rag_diagram.png)

## Part 1 — LangChain Basics

| Word | Simple Meaning |
|---|---|
| **Model** | The piece that actually talks to the AI (sends a message and gets a reply). |
| **Prompt Template** | A reusable instruction with a blank you fill in each time, e.g., `"Explain {term}"`. |
| **Output Parser** | Cleans up the AI's raw reply into the exact format you want (here: plain text). |
| **Chain (LCEL, the `\|` symbol)** | Connects steps together: *do this, then feed the result into the next step.* `prompt \| model \| parser` means "fill the prompt → send to AI → clean the reply." |
| **Memory** | Remembers earlier messages in a conversation, so the AI can understand things like "explain that again." |

**Why LangChain?**

Without it, you'd have to write all the code for sending messages, getting replies, and remembering the conversation yourself. LangChain gives you ready-made pieces that you can connect together.

### Code Walkthrough — `chain_demo.py`

#### 1. Connect to the AI Model

```python
llm = ChatGoogleGenerativeAI(model=..., google_api_key=...)
```

This is the **Model** — the connection to the AI.

#### 2. Create a Prompt Template

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You explain confusing tech words in ONE simple sentence..."),
    ("user", "{term}"),
])
```

This is the **Prompt Template**. `{term}` is the blank that gets filled with whatever word you type in.

#### 3. Create an Output Parser

```python
parser = StrOutputParser()
```

This is the **Output Parser**. It means "give me the reply as plain text."

#### 4. Connect Everything into a Chain

```python
explainer_chain = prompt | llm | parser
```

This is the **Chain**. The `|` symbol connects all three steps into one pipeline.

The process is:

1. Fill in the prompt.
2. Send it to the AI model.
3. Convert the response into plain text.

### `chain_with_memory.py` Adds Memory

```python
history = []

history.append(HumanMessage(content=term))
history.append(AIMessage(content=reply))
```

Every question and answer gets saved in a plain Python list.

For each new question, the conversation history is sent back to the AI. This helps the AI understand earlier messages and remember the conversation context.

## Part 2 — Basic RAG

**RAG (Retrieval-Augmented Generation)** means retrieving relevant information from your own documents before asking the AI to answer.

Instead of relying only on the AI's built-in knowledge, you first fetch relevant facts from your document and then give those facts to the AI along with the question. This helps ground the answer in the supplied information.

### The Main Steps of RAG

| Step | Simple Meaning |
|---|---|
| **Document Upload** | Give the app a file (here: a PDF). |
| **Chunking** | Cut the long document into small pieces because the AI cannot efficiently search one giant block of text. |
| **Embeddings** | Turn each chunk and the question into numbers that capture meaning. |
| **Vector Database** | A searchable database of those numbers (we use Chroma, which runs locally). |
| **Retrieval** | Search the vector database for the chunks most similar to the question. |
| **Grounded Answering** | Answer using only the retrieved chunks. If the answer is missing, say `"not in my documents"`. |

### Code Walkthrough — `rag/ingest.py`

This file builds the knowledge base.

#### 1. Load the PDF

```python
loader = PyPDFLoader(pdf_path)
documents = loader.load()
```

Opens the PDF and extracts its text, creating a document for each page.

#### 2. Split the Document into Chunks

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)
```

Cuts the text into chunks of 500 characters, with a 50-character overlap between consecutive chunks.

The overlap helps preserve context when information crosses chunk boundaries.

#### 3. Create Embeddings and Store Them

```python
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    ...
)

Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="db"
)
```

Turns every chunk into numbers and stores them in a local folder called `db`.

This folder contains the searchable vector database.

### Code Walkthrough — `rag/ask.py`

This file answers questions using the stored knowledge base.

#### 1. Load the Vector Database

```python
vector_store = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)
```

Reopens the saved database and creates a retriever that returns the three most relevant chunks for a question.

#### 2. Create a Grounded Prompt

```python
prompt = ChatPromptTemplate.from_template("""
Answer using ONLY the context below...

If the answer is not in the context, reply with exactly:
"not in my documents"
...
""")
```

This instruction tells the AI to answer using the supplied context rather than its general knowledge.

If the answer is not present, it must return the exact phrase `"not in my documents"`.

#### 3. Build the RAG Chain

```python
rag_chain = (
    {
        "context": retriever | format_chunks,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | parser
)
```

The complete RAG process is:

1. Retrieve the relevant document chunks.
2. Format the chunks as text.
3. Fill the prompt with the context and question.
4. Send the prompt to the AI model.
5. Convert the AI response into plain text.

## How to Run the RAG Project

Run these commands from the appropriate project directory.

```bash
# Install the required packages
pip install -r requirements.txt

# Enter the RAG folder
cd rag

# Build the knowledge base from a PDF
python ingest.py your_file.pdf

# Start asking questions
python ask.py
```

Replace `your_file.pdf` with the actual path or filename of your PDF.

**Important:** Run the installation command from the directory containing the relevant `requirements.txt` file.

## Pass Criteria

By the end of Day 3, you should be able to:

- [ ] Call an AI model through LangChain.
- [ ] Build a `prompt | model | parser` chain.
- [ ] Add conversation memory.
- [ ] Explain what RAG is and why it is useful.
- [ ] Build an app that follows this workflow: `upload document → chunk → embed → store in vector database → retrieve → answer`.
- [ ] Explain the purpose of embeddings and a vector database.
- [ ] Ensure answers are grounded in the document.
- [ ] Make the AI say `"not in my documents"` when the answer is not found in the retrieved context.

## Learn More

### 🎥 YouTube Crash Courses

**English**

- [LangChain Crash Course for Beginners](https://www.youtube.com/watch?v=lG7Uxts9SXs) — freeCodeCamp.org
- [LangChain Crash Course for Beginners | LangChain Tutorial](https://www.youtube.com/watch?v=nAmC7SoVLd8) — codebasics
- [RAG + LangChain Python Project: Easy AI/Chat for Your Docs](https://www.youtube.com/watch?v=tcqEUSNCn8I) — pixegami (approximately 20–30 minutes; closely matches this project, including chunking, embeddings, Chroma, and chatting with documents)

**Hindi**

- [Generative AI Crash Course With LangChain (3 Hours)](https://www.youtube.com/watch?v=7qqGnuRrWxg) — Krish Naik Hindi
- [Building a RAG System in LangChain | Video 15](https://www.youtube.com/watch?v=J5_-l7WIO_w) — CampusX (hands-on RAG project)

### 💻 GitHub Reference Projects

- [pixegami/langchain-rag-tutorial](https://github.com/pixegami/langchain-rag-tutorial) — A small, beginner-friendly repository for building a chat-with-your-PDF application.
- [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) — Tutorials and notebooks from the LangChain team that build RAG step by step.
- [krishnaik06/RAG-Tutorials](https://github.com/krishnaik06/RAG-Tutorials) — Reference projects accompanying Krish Naik's RAG tutorials.

### 🎓 Free Certification

- [Free Generative AI Models Course — Simplilearn SkillUp](https://www.simplilearn.com/free-generative-ai-models-course-skillup) — A free course with a certificate of completion. It covers general Generative AI fundamentals rather than LangChain specifically.