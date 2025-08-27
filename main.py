
import os, json, sys
from dotenv import load_dotenv
from tools.files import read_text_files, math_eval

load_dotenv()

try:
    from openai import OpenAI
    OPENAI = True
except Exception:
    OPENAI = False

def summarize(text: str, instruction: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if OPENAI and api_key:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise technical writer."},
                {"role": "user", "content": f"Instruction: {instruction}\n\nText:\n{text}\n\nWrite a concise, structured summary with bullet points and a short next-steps section."}
            ],
            temperature=0.2
        )
        return completion.choices[0].message.content
    else:
        # Deterministic fallback
        lines = text.splitlines()
        bullets = [f"- {ln.strip()}" for ln in lines if ln.strip()][:8]
        return "Summary (template):\n" + "\n".join(bullets) + "\n\nNext steps:\n- Add an API key for higher quality summaries."

def plan_steps(query: str):
    steps = [
        {"tool": "files.read", "args": None, "reason": "Look for local notes or context."},
        {"tool": "math.eval", "args": "2+2", "reason": "Sanity-check tool chaining with a trivial calc."},
        {"tool": "summarize", "args": query, "reason": "Compose a structured answer."}
    ]
    return steps

def run_agent(query: str):
    context_blobs = read_text_files()
    context_text = "\n\n".join([f"# {c['path']}\n{c['content']}" for c in context_blobs]) or "(no local context)"
    _ = math_eval("2+2")  # demonstration

    # First pass
    first = summarize(context_text, query)

    # Ask for "feedback" (simulated)
    feedback = "Be more specific and add 3 concrete action items."

    # Second pass refinement
    refined = first + "\n\nRefinement:\n- Action 1: Create minimal API.\n- Action 2: Add dockerfile.\n- Action 3: Add healthcheck + logging."
    return {"plan": plan_steps(query), "first_draft": first, "refined": refined, "context_files": [c['path'] for c in context_blobs]}

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py "your instruction"")
        return
    query = sys.argv[1]
    result = run_agent(query)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
