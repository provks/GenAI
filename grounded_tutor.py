"""
Grounded Tutor -- v1 (Session 01: Structured JSON outputs)
Now running on Google's Gemini API instead of OpenAI.

Ask it a question. It MUST answer in a fixed JSON shape:
    {"answer": str, "confidence": "high"|"medium"|"low", "topic": str}

This is the seed of the project we grow all course. Session 2 adds
validation + retry (guardrails). Session 3 adds memory. Sessions 5-7
add retrieval so it answers from real documents instead of just the
model's own memory (RAG).
"""

import json
import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # reads your Gemini key from .env
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")

SYSTEM_PROMPT = """You are Grounded Tutor, a terse study assistant.

Reply with ONLY a single JSON object -- no markdown fences, no text
before or after it. The object must have exactly these keys:

{
  "answer": "<your answer, max 3 sentences>",
  "confidence": "<one of: high, medium, low>",
  "topic": "<a 1-3 word tag for what this question is about>"
}

If you are not sure of the answer, say so inside "answer" and set
"confidence" to "low". Never invent facts to sound confident.
"""


def ask_tutor(question: str) -> dict:
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    raw = response.text

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logging.error("model did not return valid JSON: %r", raw)
        return {"answer": raw, "confidence": "low", "topic": "parse_error"}

    logging.info(
        "topic=%s confidence=%s prompt_tokens=%d completion_tokens=%d",
        data.get("topic"),
        data.get("confidence"),
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )
    return data


def log_interaction(question: str, result: dict, path: str = "tutor_log.jsonl") -> None:
    record = {"question": question, **result}
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def main():
    print("Grounded Tutor -- ask a question ('quit' to stop)")
    while True:
        question = input("\n> ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        if not question:
            continue
        result = ask_tutor(question)
        log_interaction(question, result)
        print(f"\n[{result.get('confidence', '?').upper()}] ({result.get('topic', '?')})")
        print(result.get("answer", "<no answer field>"))


if __name__ == "__main__":
    main()