"""
Day 3 - LangChain Basics: Models, Components, Chains

A tiny "word explainer" chain: give it a confusing tech word,
it replies with one simple sentence, no jargon.

Run it:
    python chain_demo.py
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()  # reads GEMINI_API_KEY and MODEL_NAME from your .env file

# 1. MODEL - the component that actually talks to the AI.
llm = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# 2. PROMPT TEMPLATE - a reusable instruction with a blank ({term})
#    that gets filled in every time you call the chain.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You explain confusing tech words in ONE simple sentence, "
               "like you're talking to a curious 12-year-old. No jargon."),
    ("user", "{term}"),
])

# 3. OUTPUT PARSER - cleans the AI's reply into a plain string
#    (instead of a more complex response object).
parser = StrOutputParser()

# 4. CHAIN (LCEL) - the "|" symbol connects the three pieces into
#    one pipeline: prompt (fill the blank) -> llm (get a reply)
#    -> parser (clean it up). Each step's output feeds the next step.
explainer_chain = prompt | llm | parser

if __name__ == "__main__":
    print("Word Explainer - type a confusing word, or 'quit' to stop")
    while True:
        term = input("\n> ").strip()
        if term.lower() == "quit":
            break
        if not term:
            continue
        # .invoke() runs the whole chain start to finish with this input.
        print(explainer_chain.invoke({"term": term}))
