
import os, glob

WORKSPACE = "workspace"

def read_text_files():
    files = glob.glob(os.path.join(WORKSPACE, "*"))
    results = []
    for fp in files:
        if fp.endswith((".txt", ".md")):
            with open(fp, "r", encoding="utf-8") as f:
                results.append({"path": os.path.basename(fp), "content": f.read()})
    return results

def math_eval(expr: str) -> str:
    # Very limited math evaluation for safety: numbers + operators only
    allowed = set("0123456789+-*/(). ")
    if not set(expr) <= allowed:
        return "Invalid expression."
    try:
        return str(eval(expr, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"
