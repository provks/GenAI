# Day 4 — Animated RAG Website (with Memory)

Quick, simple notes. Today you gave your RAG + memory chatbot a real website front-end instead of a plain terminal — same brain, new face.

## Picture: the full pipeline, start to finish

![Today's full pipeline](images/rag_website_pipeline_diagram.png)

## What you need to know

| Word | Simple meaning |
|---|---|
| **FastAPI** | A Python tool for building a small web server — something that listens for requests over the network and replies. |
| **Endpoint** | One specific web address your server answers at, e.g. `/ask`. |
| **CORS** | A browser safety rule. "Enabling CORS" means telling your server "it's okay, let a webpage talk to me." |
| **POST request** | The webpage sending your question to the server and waiting for a reply. |
| **Three.js** | A JavaScript library for drawing 3D graphics in a browser — what makes an animated 3D background possible. |
| **Glassmorphism** | The blurry, see-through "frosted glass" box design style. |

**Why split frontend and backend?** The backend (Python, your RAG + memory chain) is the brain — it doesn't change. The frontend (the HTML page with animations) is the face — what a visitor actually sees and clicks. They talk to each other over a local address (`http://localhost:8000`).

## What you did, step by step

1. Wrapped your existing RAG + memory chatbot in a small web server (`server.py`) with one address, `/ask`, that answers questions.
2. Built a website (`index.html`) with an animated 3D background (Three.js) and a chat box styled like frosted glass.
3. Connected the two: typing a question on the website sends it to your server, which runs it through your real chatbot and sends the answer back.
4. Tested memory on the website — asked a follow-up question that only made sense if it remembered the earlier one.

## Pass criteria

- [ ] Wrap a LangChain chain in a FastAPI endpoint
- [ ] Build an animated, 3D-styled website that calls that endpoint
- [ ] Get a grounded, memory-aware answer to show up on the website

## Learn more

### 🎥 YouTube crash courses

<!-- RESOURCES_PENDING_DAY4 -->

### 💻 GitHub reference projects

<!-- RESOURCES_PENDING_DAY4 -->

### 🎓 Free certification

<!-- RESOURCES_PENDING_DAY4 -->
