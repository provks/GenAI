# GenAI Curriculum Syllabus

From Python fundamentals to building your own Retrieval-Augmented Generation (RAG) app.

### Notes/Resources Link: https://cobalt-flannel-e18.notion.site/GenAI-3d8688695e47807d9cd8d8439bf97e82?source=copy_link
### Self Learning Resource: CampusX: https://www.youtube.com/watch?v=pSVk-5WemQ0&list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0

---

## Course Overview

| Unit | Topic | You pass this unit when you can… |
|------|-------|----------------------------------|
| 1 | **Python**: list, tuple, dict, virtual environment, pip | Set up a clean `venv`, `pip install` and freeze a `requirements.txt`, and use lists/tuples/dicts correctly without looking it up |
| 2 | **Prompt Engineering** | Take a vague prompt and make it reliable: role, clear instruction, examples, output format, and "say *I don't know*" |
| 3 | **LangChain**: models, components, document loader, text splitter, embeddings, retrievers, vector store (chromaDB), memory | Call a model through LangChain, build a `prompt \| model \| parser` chain, and add conversation memory |
| 4 | **Basic RAG** | Build an app that: uploads a doc → chunks → embeds → stores in a vector DB → retrieves → answers **grounded in the doc, and says "not in my documents" when it isn't** |

---

## Unit 1: Python Foundations

**Topics covered**
- Lists, tuples, and dictionaries
- Virtual environments (`venv`)
- Installing packages with `pip`
- Freezing dependencies to `requirements.txt`

**Pass criteria**
- Create and activate a clean `venv`
- Run `pip install` and `pip freeze > requirements.txt`
- Use lists, tuples, and dicts correctly without looking anything up

---

## Unit 2: Prompt Engineering

**Topics covered**
- Assigning a role
- Writing clear instructions
- Using examples (few-shot prompting)
- Specifying an output format
- Handling uncertainty ("say *I don't know*")

**Pass criteria**
- Take a vague prompt and rewrite it to be reliable and consistent, using all five techniques taught in class(check notes).

---

## Unit 3: LangChain

**Topics covered**
- Models
- Components (prompts, parsers)
- Chains
- Memory

**Pass criteria**
- Call a model through LangChain
- Build a `prompt | model | parser` chain
- Add conversation memory

---

## Unit 4: Basic RAG

**Topics covered**
- Document upload
- Chunking
- Embeddings
- Vector databases
- Retrieval
- Grounded answering

**Pass criteria**
- Build an app that follows this pipeline:

  `upload doc → chunk → embed → store in vector DB → retrieve → answer`

- Answers must be **grounded in the document**
- The app must say **"not in my documents"** when the answer isn't found

---

## Recommended Videos (LangChain)

The LangChain notes follow these free videos from CampusX. Use the table below to match each section of the notes to its video. The full series is also available as a [playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0).

| Notes section | Topic | Video(s) | Time |
|---------------|-------|----------|------|
| 0–1 | What & components | [Introduction to LangChain](https://www.youtube.com/watch?v=nlz9j-r0U9U) · [LangChain Components](https://www.youtube.com/watch?v=-xSJA8-o6Eg) | 38 + 53 min |
| 2 | Models | [LangChain Models](https://www.youtube.com/watch?v=HdcLE8JuMrA) *(skim)* | 102 min |
| 3 | Prompts | [Prompts in LangChain](https://www.youtube.com/watch?v=3TGqlQxpuU0) | 79 min |
| 4 | Output parsers | [Structured Output](https://www.youtube.com/watch?v=y5EmRr1O1h4) · [Output Parsers](https://www.youtube.com/watch?v=Op6PbJZ5b2Q) | 68 + 53 min |
| 5 | Chains / LCEL | [Chains in LangChain](https://youtu.be/5hjrPILA3-8) · [Runnables (Part 1)](https://www.youtube.com/watch?v=u3b-W1NgYa4) · [Runnables (Part 2)](https://www.youtube.com/watch?v=47nc0n-e4_w) | 54 + 76 + 54 min |

**Total viewing time:** roughly 9.5 hours (about 8 hours if you skim the Models video as suggested).

---


## How You'll Be Assessed

Each unit is pass/fail based on the criteria above. Be ready to demonstrate your work live or submit your code and a short demo.

## Prerequisites

- A laptop with Python 3.10+ installed
- A code editor (e.g., VS Code)
- An API key for an LLM provider (details shared in class)
