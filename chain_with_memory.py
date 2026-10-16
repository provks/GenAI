"""
Day 3 - LangChain Basics: Adding Memory

Same word-explainer idea as chain_demo.py, but now it REMEMBERS
earlier turns in the conversation. Try asking "explain that again
even simpler" after your first question - it will know what "that"
means, because the earlier messages are sent back in every time.

Run it:
    python chain_with_memory.py
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You explain confusing tech words in ONE simple sentence. No jargon."),
    # MessagesPlaceholder marks the spot where all the earlier
    # conversation messages get inserted, before the new question.
    MessagesPlaceholder("history"),
    ("user", "{term}"),
])

parser = StrOutputParser()
chain = prompt | llm | parser

# MEMORY - the simplest possible version: just a plain Python list
# that stores every message so far. Every turn, we hand the whole
# list back to the chain, so the AI "remembers" the conversation.
history = []

if __name__ == "__main__":
    print("Word Explainer with Memory - type 'quit' to stop")
    while True:
        term = input("\n> ").strip()
        if term.lower() == "quit":
            break
        if not term:
            continue

        reply = chain.invoke({"term": term, "history": history})
        print(reply)

        # Save this turn into memory, so the next question can refer
        # back to it (e.g. "simplify that further").
        history.append(HumanMessage(content=term))
        history.append(AIMessage(content=reply))
