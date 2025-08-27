
# Agentic Research Assistant (LangChain)

A simple **agent-style** assistant that plans → calls tools → summarizes → asks for feedback → refines.
Tools included:
- Local file reader (reads `.md`/`.txt` from `workspace/`)
- Math (safe eval for basic arithmetic)
- Optional LLM for final summaries (OpenAI) — or a deterministic template if no key.

This is intentionally small but shows agent loop + tool calls + reflection.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Put files to "research" into workspace/
echo "FastAPI is a modern, fast Python web framework." > workspace/fastapi_notes.txt

python main.py "Summarize what FastAPI is and suggest a deployment plan."
```

## Notes
- If no OpenAI key is set, you still get a working pipeline with a deterministic summarizer (template-based).
- For a web-search tool, you can add a SerpAPI tool quickly — omitted to keep setup simple.
