# Day 2 — Prompt Engineering

Quick, simple notes. The project for this day is `grounded_tutor.py` in this folder.

## What You Need to Know

**Prompt engineering** = writing your instructions to the AI carefully, so it gives you reliable, useful answers instead of random or made-up ones.

Five techniques:

| Technique | Simple Meaning | In `grounded_tutor.py` |
|---|---|---|
| **1. Assign a role** | Tell the AI *who it is* before asking anything. | `"You are Grounded Tutor, a terse study assistant."` |
| **2. Write clear instructions** | Say exactly what you want, not vaguely. | `"Reply with ONLY a single JSON object — no markdown fences, no text before or after it."` |
| **3. Few-shot prompting** | Give the AI 1–2 *examples* of a correct answer, so it copies the pattern. | *Not used in this file* — see the mini-example below. |
| **4. Specify output format** | Show the AI the exact shape you want the answer in. | The JSON shape with `answer`, `confidence`, and `topic` keys. |
| **5. Handle uncertainty** | Tell the AI it's okay to say "I don't know" instead of guessing. | `"If you are not sure of the answer, say so... Never invent facts to sound confident."` |

### Mini-Example of Few-Shot Prompting (Technique 3)

This technique is not used in `grounded_tutor.py`.

```text
Turn this into a polite email:

Input: "send report now"
Output: "Hi, could you please send the report when you get a chance? Thanks!"

Input: "meeting moved to 3pm"
Output:
```

Giving the AI one or more examples before your real question is called **few-shot prompting**.

- **Zero-shot prompting:** No examples are provided.
- **Few-shot prompting:** One or more examples are provided.

## Code Walkthrough — `grounded_tutor.py`

Line-by-line explanations of the important parts.

### 1. Connect to Gemini

```python
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

Connects to Google's Gemini AI using your API key. The key is stored in a `.env` file or environment variable instead of being typed directly into the code.

### 2. Select the AI Model

```python
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")
```

Picks which AI model to use. If `MODEL_NAME` is not set, the code defaults to `gemini-2.5-flash`.

### 3. Create the System Prompt

```python
SYSTEM_PROMPT = """You are Grounded Tutor, a terse study assistant. ..."""
```

This contains the **role, instructions, output format, and uncertainty rule** in one block of text.

This is prompt engineering in action.

### 4. Send a Question to the AI

```python
def ask_tutor(question: str) -> dict:
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        ),
    )
    raw = response.text
```

This function:

1. Accepts a question from the user.
2. Sends the question and system prompt to Gemini.
3. Receives the AI's response as raw text.

### 5. Handle Invalid JSON

```python
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logging.error("model did not return valid JSON: %r", raw)
        return {
            "answer": raw,
            "confidence": "low",
            "topic": "parse_error"
        }
```

This tries to read the AI's response as JSON.

If the response is not valid JSON, the code catches the error instead of crashing the program and returns a fallback response.

### 6. Log the Response Details

```python
    logging.info(
        "topic=%s confidence=%s prompt_tokens=%d completion_tokens=%d",
        data.get("topic"),
        data.get("confidence"),
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )
    return data
```

This records useful information for debugging and tracking, including:

- The topic of the answer.
- The confidence level.
- The number of prompt tokens.
- The number of completion tokens.

Finally, it returns the structured answer.

### 7. Save Each Interaction

```python
def log_interaction(question, result, path="tutor_log.jsonl"):
    record = {"question": question, **result}
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")
```

This saves each question and its answer in a log file called `tutor_log.jsonl`.

Each interaction is stored as a separate JSON object on a new line.

### 8. Run the Main Program

```python
def main():
    print("Grounded Tutor -- ask a question ('quit' to stop)")

    while True:
        question = input("\n> ").strip()

        if question.lower() in {"quit", "exit"}:
            break

        ...
```

The main loop repeatedly asks the user to enter a question.

The program continues until the user types `quit` or `exit`.

## Pass Criteria

By the end of Day 2, you should be able to:

- [ ] Take a vague prompt and rewrite it into a reliable prompt.
- [ ] Use all five prompt engineering techniques.
- [ ] Explain the purpose of a system prompt.
- [ ] Understand how structured JSON output works.
- [ ] Explain why handling uncertainty is important.
- [ ] Understand how `grounded_tutor.py` sends questions to Gemini and processes responses.

## Learn More

### 🎥 YouTube Crash Courses

**English**

- [Prompt Engineering Tutorial – Master ChatGPT and LLM Responses](https://www.youtube.com/watch?v=_ZvnD73m40o) — freeCodeCamp.org (approximately 1 hour)
- [RAG vs Fine-Tuning vs Prompt Engineering: Optimizing AI Models](https://www.youtube.com/watch?v=zYGDpG-pTho) — IBM Technology (approximately 11 minutes)
- [Master the Perfect ChatGPT Prompt Formula (in Just 8 Minutes!)](https://www.youtube.com/watch?v=jC4v5AS4RIM) — Jeff Su (approximately 8 minutes)
- [Master Prompt Engineering in 11 Minutes](https://www.youtube.com/watch?v=zSyo6YtdLnI) — Simplilearn (approximately 11 minutes)

**Hindi**

- [ChatGPT Prompt Engineering Course for Beginners in Hindi](https://www.youtube.com/watch?v=sFD35B_fIuM) — HBA Services

### 💻 GitHub Reference Projects

- [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) — A beginner-to-advanced reference covering roles, clear instructions, few-shot prompting, and output formatting.
- [google-gemini/cookbook — JSON Mode Quickstart](https://github.com/google-gemini/cookbook/blob/main/quickstarts/JSON_mode.ipynb) — Google's example notebook for structured JSON output from Gemini.
- [openai/openai-cookbook](https://github.com/openai/openai-cookbook) — Prompting examples and practical patterns. Many concepts apply across AI models.

### 🎓 Free Certification

- [Introduction to Prompt Engineering Fundamentals — Simplilearn SkillUp](https://www.simplilearn.com/prompt-engineering-free-course-skillup) — A free course with a certificate of completion.

---

# Day 1 — Python Foundations

Quick, simple notes. No long explanations — just what you need to know and practice.

## What You Need to Know

### Lists, Tuples, and Dictionaries

| Thing | What It Is | Example |
|---|---|---|
| **List** | An ordered group of items you can change by adding, removing, or editing them. | `fruits = ["apple", "banana", "mango"]` |
| **Tuple** | An ordered group of items that cannot be changed after creation. | `point = (10, 20)` |
| **Dictionary** | A group of `key: value` pairs, like a real dictionary that maps a word to its meaning. | `student = {"name": "Ravi", "age": 20}` |

**When to use which:**

- **List:** Use it when the data can change.
- **Tuple:** Use it when the collection should remain unchanged, such as a pair of coordinates.
- **Dictionary:** Use it when you want to look up values by name instead of by position.

### Virtual Environment (`venv`)

A **virtual environment** is a clean, separate environment for one project's Python packages. It helps prevent packages installed for one project from interfering with another project.

```bash
# Create a virtual environment (one-time per project)
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows Command Prompt
venv\Scripts\activate

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

You'll know the environment is active when your terminal prompt usually starts with `(venv)`.

### `pip` — Installing Packages

`pip` is Python's package installer. It downloads and installs packages created by other developers so you don't have to write everything yourself.

```bash
pip install requests
```

### `requirements.txt` — Managing Dependencies

A `requirements.txt` file lists the Python packages a project needs. You can use it to recreate the project's package environment on another computer.

```bash
# Save installed packages and their versions
pip freeze > requirements.txt

# Install packages listed in the file
pip install -r requirements.txt
```

## Pass Criteria

By the end of Day 1, you should be able to:

- [ ] Create and activate a clean virtual environment (`venv`).
- [ ] Install a package using `pip`.
- [ ] Save dependencies using `pip freeze > requirements.txt`.
- [ ] Install dependencies using `pip install -r requirements.txt`.
- [ ] Use lists, tuples, and dictionaries correctly without looking anything up.

## Learn More

### 🎥 YouTube Crash Courses

**English**

- [Python Tutorial for Beginners 4: Lists, Tuples, and Sets](https://www.youtube.com/watch?v=W8KRzm-HUcc) — Corey Schafer (approximately 29 minutes)
- [Python Tutorial: VENV — How to Use Virtual Environments](https://www.youtube.com/watch?v=APOPm01BVrk) — Corey Schafer (approximately 17 minutes)

**Hindi**

- [Lecture 3: List and Tuple in Python | Python Full Course](https://www.youtube.com/watch?v=qVyvmzFxF_o) — Apna College (approximately 41 minutes)
- [Lecture 4: Dictionary and Set in Python | Python Full Course](https://www.youtube.com/watch?v=078tYSD7K8E) — Apna College (approximately 54 minutes)
- [Virtual Environment and requirements.txt | Python Tutorials for Absolute Beginners #43](https://www.youtube.com/watch?v=Lah7WGW6exg) — CodeWithHarry (approximately 21 minutes)

### 💻 GitHub Reference Projects

- [trekhleb/learn-python](https://github.com/trekhleb/learn-python) — A collection of annotated Python examples, including lists, tuples, dictionaries, and other Python fundamentals.
- [navdeep-G/samplemod](https://github.com/navdeep-G/samplemod) — An example Python project structure that demonstrates packaging and project organization.

### 🎓 Free Certification

- [Python for Beginners — Simplilearn SkillUp](https://www.simplilearn.com/learn-python-basics-free-course-skillup) — A beginner-friendly Python course with a certificate of completion.

---

**Note:** Day 2 appears before Day 1 because that was the order in your original content. You can reverse the sections if you want the file to follow the learning sequence.