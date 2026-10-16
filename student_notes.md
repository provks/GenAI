# Day 2 — Prompt Engineering

Quick, simple notes. The project for this day is `grounded_tutor.py` in this folder.

## What you need to know

**Prompt engineering** = writing your instructions to the AI carefully, so it gives you reliable, useful answers instead of random or made-up ones. Five techniques:

| Technique | Simple meaning | In `grounded_tutor.py` |
|---|---|---|
| **1. Assign a role** | Tell the AI *who it is* before asking anything. | `"You are Grounded Tutor, a terse study assistant."` |
| **2. Write clear instructions** | Say exactly what you want, not vaguely. | "Reply with ONLY a single JSON object — no markdown fences, no text before or after it." |
| **3. Few-shot prompting** | Give the AI 1-2 *examples* of a correct answer, so it copies the pattern. | *Not used in this file* — see mini-example below. |
| **4. Specify output format** | Show the AI the exact shape you want the answer in. | The JSON shape with `answer`, `confidence`, `topic` keys. |
| **5. Handle uncertainty** | Tell the AI it's okay to say "I don't know" instead of guessing. | "If you are not sure of the answer, say so... Never invent facts to sound confident." |

### Mini-example of few-shot prompting (technique 3, not in the file)

```
Turn this into a polite email:
Input: "send report now"
Output: "Hi, could you please send the report when you get a chance? Thanks!"

Input: "meeting moved to 3pm"
Output:
```

Giving the AI 1 example (or more) before your real question is "few-shot." Zero examples = "zero-shot."

## Code walkthrough — `grounded_tutor.py`, line by line (the important parts)

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```
Connects to Google's Gemini AI using your API key (kept secretly in a `.env` file, never typed directly in code).

```python
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")
```
Picks which AI model to use. If no model is set in `.env`, it defaults to `gemini-2.5-flash`.

```python
SYSTEM_PROMPT = """You are Grounded Tutor, a terse study assistant. ..."""
```
This is the **role + instructions + output format + uncertainty rule**, all in one block of text — this is "prompt engineering" in action.

```python
def ask_tutor(question: str) -> dict:
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    raw = response.text
```
Sends your question + the system prompt to the AI, and gets back its raw text reply.

```python
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logging.error("model did not return valid JSON: %r", raw)
        return {"answer": raw, "confidence": "low", "topic": "parse_error"}
```
Tries to read the AI's reply as JSON. If the AI messed up the format, this catches the error instead of crashing the program, and returns a safe fallback.

```python
    logging.info(
        "topic=%s confidence=%s prompt_tokens=%d completion_tokens=%d",
        data.get("topic"), data.get("confidence"),
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )
    return data
```
Logs what happened (for debugging/tracking) and returns the structured answer.

```python
def log_interaction(question, result, path="tutor_log.jsonl"):
    record = {"question": question, **result}
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")
```
Saves every question + answer to a log file, one line per interaction — so you have a record of everything asked.

```python
def main():
    print("Grounded Tutor -- ask a question ('quit' to stop)")
    while True:
        question = input("\n> ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        ...
```
The main loop: keeps asking you for a question until you type `quit`.

## Pass criteria (what you should be able to do)

- [ ] Take a vague prompt and rewrite it to be reliable, using all 5 techniques above

## Learn more

### 🎥 YouTube crash courses

<!-- RESOURCES_PENDING_DAY2 -->

### 💻 GitHub reference projects

<!-- RESOURCES_PENDING_DAY2 -->

### 🎓 Free certification

<!-- RESOURCES_PENDING_DAY2 -->
